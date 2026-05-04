from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.retrieval.norm_parser import extract_norm_refs


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    context_text: str
    norm_label: str
    law_abbr: str
    version_id: str
    score: float


def reciprocal_rank_fusion(result_lists: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for results in result_lists:
        for rank, chunk_id in enumerate(results, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


class RetrievalOrchestrator:
    def __init__(self):
        self._chunks = [
            RetrievedChunk(
                chunk_id="vwvfg_35_abs1",
                text="Ein Verwaltungsakt ist jede Verfügung, Entscheidung oder andere hoheitliche Maßnahme.",
                context_text="VwVfG § 35",
                norm_label="§ 35",
                law_abbr="VwVfG",
                version_id="vwvfg_2024_01_01",
                score=0.0,
            ),
            RetrievedChunk(
                chunk_id="vwvfg_39_abs1",
                text="Ein schriftlicher Verwaltungsakt ist schriftlich zu begründen.",
                context_text="VwVfG § 39",
                norm_label="§ 39",
                law_abbr="VwVfG",
                version_id="vwvfg_2024_01_01",
                score=0.0,
            ),
        ]

    def retrieve(self, query: str, effective_date: date, limit: int = 10) -> tuple[list[RetrievedChunk], dict]:
        _ = effective_date
        refs = extract_norm_refs(query)

        exact_ids = [
            c.chunk_id
            for c in self._chunks
            if any(ref.norm_label == c.norm_label and (ref.law_abbr is None or ref.law_abbr == c.law_abbr) for ref in refs)
        ]

        q_terms = query.lower().split()
        bm25_ids: list[str] = []
        if q_terms:
            bm25_ids = [c.chunk_id for c in self._chunks if any(term in c.text.lower() for term in q_terms)]

        dense_ids: list[str] = []
        fused = reciprocal_rank_fusion([exact_ids, bm25_ids, dense_ids])
        selected_ids = [chunk_id for chunk_id, _ in fused[:limit]]

        chunk_map = {chunk.chunk_id: chunk for chunk in self._chunks}
        selected = [chunk_map[cid] for cid in selected_ids if cid in chunk_map]

        trace = {
            "norm_refs": [r.__dict__ for r in refs],
            "exact_ids": exact_ids,
            "bm25_ids": bm25_ids,
            "dense_ids": dense_ids,
            "fused": fused,
            "selected": [c.chunk_id for c in selected],
        }
        return selected, trace

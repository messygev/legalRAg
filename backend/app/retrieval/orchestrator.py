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
    def retrieve(self, query: str, effective_date: date, limit: int = 10) -> tuple[list[RetrievedChunk], dict]:
        _ = effective_date
        refs = extract_norm_refs(query)
        trace = {
            "norm_refs": [r.__dict__ for r in refs],
            "exact_ids": [],
            "bm25_ids": [],
            "dense_ids": [],
            "selected": [],
        }
        return [], trace

from __future__ import annotations

from dataclasses import dataclass

from app.retrieval.norm_parser import extract_norm_refs


@dataclass
class NoticeNormMention:
    raw_mention: str
    normalized_norm: str | None
    law_abbr: str | None
    norm_label: str | None
    confidence: float


def extract_notice_norm_mentions(text: str) -> list[NoticeNormMention]:
    refs = extract_norm_refs(text)
    return [
        NoticeNormMention(
            raw_mention=r.raw,
            normalized_norm=f"{r.norm_label} {r.law_abbr}" if r.law_abbr else r.norm_label,
            law_abbr=r.law_abbr,
            norm_label=r.norm_label,
            confidence=0.9 if r.law_abbr else 0.7,
        )
        for r in refs
    ]

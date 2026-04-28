from __future__ import annotations

import re
from dataclasses import dataclass

ADVICE_PATTERNS = [
    r"\b[Ss]ie sollten\b",
    r"\b[Ii]ch empfehle\b",
    r"\b[Ee]s ist ratsam\b",
    r"\b[Ss]ie haben Anspruch auf\b",
    r"\b[Dd]as ist rechtswidrig\b",
    r"\b[Kk]lagen Sie\b",
    r"\b[Ll]egen Sie Widerspruch ein\b",
]
CHUNK_ID_RE = re.compile(r"chunk_id=([A-Za-z0-9_\-]+)")


@dataclass
class ValidationResult:
    passed: bool
    reason: str | None = None


def extract_cited_chunk_ids(answer: str) -> set[str]:
    return set(CHUNK_ID_RE.findall(answer))


def contains_advice(answer: str) -> bool:
    return any(re.search(pattern, answer) for pattern in ADVICE_PATTERNS)


def validate_answer(answer: str, allowed_chunk_ids: set[str]) -> ValidationResult:
    if not answer or not answer.strip():
        return ValidationResult(False, "empty_answer")
    if "Die bereitgestellten Quellen reichen" in answer:
        return ValidationResult(True, "abstained")
    if contains_advice(answer):
        return ValidationResult(False, "legal_advice_detected")
    cited = extract_cited_chunk_ids(answer)
    if not cited:
        return ValidationResult(False, "missing_citations")
    if not cited.issubset(allowed_chunk_ids):
        return ValidationResult(False, "unknown_chunk_cited")
    return ValidationResult(True)

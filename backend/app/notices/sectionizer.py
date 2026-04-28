from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NoticeSection:
    section_type: str
    text: str
    confidence: float


HEADINGS = {
    "tenor": ["bescheid", "verfügung", "entscheidung", "tenor"],
    "reasoning": ["begründung", "gründe", "sachverhalt"],
    "legal_remedy": ["rechtsbehelfsbelehrung", "rechtsmittelbelehrung"],
}


def sectionize_notice(text: str) -> list[NoticeSection]:
    lines = text.splitlines()
    sections: list[NoticeSection] = []
    current_type = "unknown"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        content = "\n".join(current_lines).strip()
        if content:
            conf = 0.65 if current_type != "unknown" else 0.4
            sections.append(NoticeSection(current_type, content, conf))
        current_lines = []

    for line in lines:
        normalized = line.strip().lower().rstrip(":")
        matched = None
        for st, headings in HEADINGS.items():
            if normalized in headings or any(normalized.startswith(h) for h in headings):
                matched = st
                break
        if matched:
            flush()
            current_type = matched
        current_lines.append(line)
    flush()
    return sections or [NoticeSection("unknown", text, 0.3)]

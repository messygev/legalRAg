from __future__ import annotations

import re
from dataclasses import dataclass

DATE_RE = re.compile(r"\b(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})\b")
FILE_NUMBER_RE = re.compile(r"(?:Az\.|Aktenzeichen)\s*[: ]\s*([A-Za-z0-9/\- .]+)")


@dataclass
class ExtractedField:
    name: str
    value: str | None
    normalized_value: str | None
    confidence: float


def extract_notice_fields(text: str) -> list[ExtractedField]:
    fields: list[ExtractedField] = []
    m = FILE_NUMBER_RE.search(text)
    if m:
        value = m.group(1).strip()
        fields.append(ExtractedField("file_number", value, value, 0.85))

    dates = list(DATE_RE.finditer(text))
    if dates:
        d = dates[0]
        normalized = f"{d.group('year')}-{int(d.group('month')):02d}-{int(d.group('day')):02d}"
        fields.append(ExtractedField("notice_date", d.group(0), normalized, 0.65))

    for line in text.splitlines()[:20]:
        l = line.strip()
        if any(t in l.lower() for t in ["landratsamt", "stadt", "gemeinde", "behörde", "amt"]):
            fields.append(ExtractedField("authority", l, l, 0.7))
            break
    return fields

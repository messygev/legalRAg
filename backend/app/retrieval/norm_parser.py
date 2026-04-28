from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class NormRef:
    raw: str
    law_abbr: str | None
    norm_label: str
    article_type: str
    paragraph: str | None = None
    sentence: str | None = None
    number: str | None = None


NORM_RE = re.compile(
    r"(?P<prefix>§{1,2}|Art\.?|Artikel)\s*"
    r"(?P<num>[0-9]+[a-zA-Z]?)"
    r"(?:\s*(?:Abs\.|Absatz)\s*(?P<abs>[0-9]+[a-zA-Z]?))?"
    r"(?:\s*(?:S\.|Satz)\s*(?P<satz>[0-9]+))?"
    r"(?:\s*(?:Nr\.|Nummer)\s*(?P<nr>[0-9]+[a-zA-Z]?))?"
    r"(?:\s*(?P<law>[A-ZÄÖÜ][A-Za-zÄÖÜäöüß0-9\-]{1,30}))?"
)


def normalize_prefix(prefix: str) -> str:
    return "paragraph" if prefix.startswith("§") else "article"


def normalize_norm_label(prefix: str, num: str) -> str:
    if prefix.startswith("§"):
        return f"§ {num}"
    return f"Art. {num}"


def extract_norm_refs(text: str) -> list[NormRef]:
    refs: list[NormRef] = []
    for match in NORM_RE.finditer(text):
        prefix = match.group("prefix")
        num = match.group("num")
        refs.append(
            NormRef(
                raw=match.group(0),
                law_abbr=match.group("law"),
                norm_label=normalize_norm_label(prefix, num),
                article_type=normalize_prefix(prefix),
                paragraph=match.group("abs"),
                sentence=match.group("satz"),
                number=match.group("nr"),
            )
        )
    return refs

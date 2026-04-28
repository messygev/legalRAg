from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChecklistItem:
    check_key: str
    check_label: str
    status: str
    risk_level: str
    explanation: str
    basis_norm_label: str | None
    basis_chunk_id: str | None
    confidence: float


def build_notice_checklist(sections, fields, norm_mentions, matched_basis) -> list[ChecklistItem]:
    section_types = {s.section_type for s in sections}
    field_names = {f.name for f in fields}
    norm_labels = {m.norm_label for m in norm_mentions if m.norm_label}
    return [
        ChecklistItem(
            "administrative_act_detected",
            "Verwaltungsakt erkennbar",
            "detected" if ("tenor" in section_types or "§ 35" in norm_labels) else "unclear",
            "low" if ("tenor" in section_types or "§ 35" in norm_labels) else "medium",
            "Tenor oder Bezug zu § 35 VwVfG erkannt." if ("tenor" in section_types or "§ 35" in norm_labels) else "Kein eindeutiger Tenor oder § 35-Bezug erkannt.",
            "§ 35 VwVfG",
            matched_basis.get("§ 35 VwVfG"),
            0.8,
        ),
        ChecklistItem(
            "reasoning_present",
            "Begründung vorhanden",
            "detected" if "reasoning" in section_types else "unclear",
            "low" if "reasoning" in section_types else "medium",
            "Abschnitt Begründung/Gründe wurde erkannt." if "reasoning" in section_types else "Kein eindeutiger Begründungsabschnitt erkannt.",
            "§ 39 VwVfG",
            matched_basis.get("§ 39 VwVfG"),
            0.75 if "reasoning" in section_types else 0.5,
        ),
        ChecklistItem(
            "legal_remedy_present", "Rechtsbehelfsbelehrung vorhanden",
            "detected" if "legal_remedy" in section_types else "unclear",
            "low" if "legal_remedy" in section_types else "medium",
            "Rechtsbehelfsbelehrung wurde erkannt." if "legal_remedy" in section_types else "Keine eindeutige Rechtsbehelfsbelehrung erkannt.",
            None, None, 0.8 if "legal_remedy" in section_types else 0.45,
        ),
        ChecklistItem(
            "notice_date_detected", "Bescheiddatum erkannt",
            "detected" if "notice_date" in field_names else "missing",
            "low" if "notice_date" in field_names else "medium",
            "Bescheiddatum wurde extrahiert." if "notice_date" in field_names else "Kein Bescheiddatum erkannt.",
            None, None, 0.7 if "notice_date" in field_names else 0.4,
        ),
    ]

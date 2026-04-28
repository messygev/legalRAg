from __future__ import annotations

from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field


class NoticeAnalyzeTextRequest(BaseModel):
    text: str = Field(min_length=20, max_length=200_000)
    received_date: date | None = None
    effective_date: date


class FieldValue(BaseModel):
    value: str | None
    confidence: float


class NoticeSectionResponse(BaseModel):
    section_type: str
    confidence: float
    text_preview: str


class NormMentionResponse(BaseModel):
    raw_mention: str
    normalized_norm: str | None
    matched_chunk_id: str | None
    confidence: float


class ChecklistItemResponse(BaseModel):
    check_key: str
    check_label: str
    status: str
    risk_level: str
    basis: str | None = None
    basis_chunk_id: str | None = None
    confidence: float


class DeadlineResponse(BaseModel):
    deadline_type: str
    calculation_status: str
    anchor_date: date | None = None
    calculated_date: date | None = None
    explanation: str


class NoticeAnalyzeResponse(BaseModel):
    notice_id: UUID
    document_type: str | None
    detected_fields: dict[str, FieldValue]
    sections: list[NoticeSectionResponse]
    norm_mentions: list[NormMentionResponse]
    checklist: list[ChecklistItemResponse]
    deadlines: list[DeadlineResponse]
    disclaimer: str = "Keine Rechtsberatung. Nur strukturierte, beleggestützte Analysehilfe."

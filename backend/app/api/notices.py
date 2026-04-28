from __future__ import annotations

from datetime import date
from uuid import uuid4

from fastapi import APIRouter

from app.notices.checklist import build_notice_checklist
from app.notices.deadline import calculate_one_month_deadline
from app.notices.extractor import extract_notice_fields
from app.notices.norm_mentions import extract_notice_norm_mentions
from app.notices.injection_filter import sanitize_untrusted_document_text
from app.notices.sectionizer import sectionize_notice
from app.schemas.notice import (
    ChecklistItemResponse,
    DeadlineResponse,
    FieldValue,
    NormMentionResponse,
    NoticeAnalyzeResponse,
    NoticeAnalyzeTextRequest,
    NoticeSectionResponse,
)

router = APIRouter(prefix="/v1/notices")


@router.post("/analyze-text", response_model=NoticeAnalyzeResponse)
def analyze_text(request: NoticeAnalyzeTextRequest) -> NoticeAnalyzeResponse:
    sanitized_text, _injection_findings = sanitize_untrusted_document_text(request.text)
    sections = sectionize_notice(sanitized_text)
    fields = extract_notice_fields(sanitized_text)
    mentions = extract_notice_norm_mentions(sanitized_text)
    checklist = build_notice_checklist(sections, fields, mentions, matched_basis={})
    anchor = request.received_date or date.today()
    deadline = calculate_one_month_deadline(anchor)

    return NoticeAnalyzeResponse(
        notice_id=uuid4(),
        document_type="verwaltungsbescheid",
        detected_fields={f.name: FieldValue(value=f.value, confidence=f.confidence) for f in fields},
        sections=[NoticeSectionResponse(section_type=s.section_type, confidence=s.confidence, text_preview=s.text[:200]) for s in sections],
        norm_mentions=[NormMentionResponse(raw_mention=m.raw_mention, normalized_norm=m.normalized_norm, matched_chunk_id=None, confidence=m.confidence) for m in mentions],
        checklist=[ChecklistItemResponse(check_key=i.check_key, check_label=i.check_label, status=i.status, risk_level=i.risk_level, basis=i.basis_norm_label, basis_chunk_id=i.basis_chunk_id, confidence=i.confidence) for i in checklist],
        deadlines=[DeadlineResponse(deadline_type=deadline.deadline_type, calculation_status=deadline.calculation_status, anchor_date=deadline.anchor_date, calculated_date=deadline.calculated_date, explanation=deadline.explanation)],
    )

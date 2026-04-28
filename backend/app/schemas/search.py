from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    effective_date: date
    mode: str = Field(default="research", pattern="^(research|compare|definition)$")


class SourceSchema(BaseModel):
    chunk_id: str
    norm: str
    eli: str | None = None
    version_id: str
    valid_from: date | None = None
    valid_to: date | None = None


class SearchResponse(BaseModel):
    answer: str | None
    status: str
    reason: str | None = None
    sources: list[SourceSchema]
    retrieval_trace_id: str
    disclaimer: str = "Keine Rechtsberatung. Nur beleggestützte Rechercheauskunft."

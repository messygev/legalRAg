from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter

from app.schemas.search import SearchRequest, SearchResponse

router = APIRouter(prefix="/v1")


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    return SearchResponse(
        answer=None,
        status="abstained",
        reason="insufficient_evidence",
        sources=[],
        retrieval_trace_id=str(uuid4()),
    )

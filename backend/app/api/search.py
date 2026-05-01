from __future__ import annotations

from fastapi import APIRouter

from app.agentic.models import AgentContext
from app.agentic.orchestrator import AgentOrchestrator
from app.audit_store import write_answer_audit, write_retrieval_log
from app.schemas.search import SearchRequest, SearchResponse, SourceSchema

router = APIRouter(prefix="/v1")
agent = AgentOrchestrator()


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    run = agent.run(AgentContext(query=request.query, effective_date=request.effective_date, mode=request.mode))
    retrieval_log_id = write_retrieval_log(
        {"query": request.query, "effective_date": request.effective_date.isoformat(), "trace": run.trace}
    )
    write_answer_audit(
        {
            "retrieval_log_id": retrieval_log_id,
            "query": request.query,
            "status": run.status,
            "reason": run.reason,
            "cited_chunk_ids": run.cited_chunk_ids,
        }
    )

    return SearchResponse(
        answer=run.answer,
        status=run.status,
        reason=run.reason,
        sources=[
            SourceSchema(
                chunk_id=s["chunk_id"],
                norm=s["norm"],
                eli=s.get("eli"),
                version_id=s["version_id"],
                valid_from=s.get("valid_from"),
                valid_to=s.get("valid_to"),
            )
            for s in run.source_records
        ],
        retrieval_trace_id=retrieval_log_id,
    )

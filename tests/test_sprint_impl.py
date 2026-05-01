from datetime import date

from app.retrieval.orchestrator import RetrievalOrchestrator


def test_retrieval_handles_empty_query():
    chunks, trace = RetrievalOrchestrator().retrieve("", effective_date=date(2026, 1, 1))
    assert isinstance(chunks, list)
    assert "bm25_ids" in trace

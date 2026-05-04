from datetime import date

from app.retrieval.orchestrator import RetrievalOrchestrator


def test_retrieve_norm_exact_match():
    chunks, trace = RetrievalOrchestrator().retrieve("§ 35 VwVfG", effective_date=date(2026, 1, 1))
    assert chunks
    assert chunks[0].chunk_id == "vwvfg_35_abs1"
    assert "vwvfg_35_abs1" in trace["selected"]


def test_retrieve_keyword_match():
    chunks, _ = RetrievalOrchestrator().retrieve("begründen", effective_date=date(2026, 1, 1))
    assert any(c.chunk_id == "vwvfg_39_abs1" for c in chunks)

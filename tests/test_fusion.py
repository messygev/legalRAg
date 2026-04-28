from app.retrieval.orchestrator import reciprocal_rank_fusion


def test_rrf_orders_shared_hits_higher():
    fused = reciprocal_rank_fusion([["a", "b"], ["a", "c"]])
    assert fused[0][0] == "a"

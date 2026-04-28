from app.llm.validators import validate_answer


def test_validate_blocks_advice():
    res = validate_answer("Sie sollten klagen.", {"c1"})
    assert not res.passed
    assert res.reason == "legal_advice_detected"


def test_validate_allows_abstention():
    res = validate_answer("Die bereitgestellten Quellen reichen für eine belegte Antwort nicht aus.", set())
    assert res.passed

from app.notices.sectionizer import sectionize_notice


def test_notice_sections_detected():
    text = """Bescheid\nBegründung:\nX\nRechtsbehelfsbelehrung:\nY"""
    types = {s.section_type for s in sectionize_notice(text)}
    assert "reasoning" in types
    assert "legal_remedy" in types

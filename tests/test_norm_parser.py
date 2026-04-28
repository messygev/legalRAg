from app.retrieval.norm_parser import extract_norm_refs


def test_extract_vwvfg():
    refs = extract_norm_refs("§ 35 Abs. 1 Satz 1 VwVfG")
    assert refs[0].norm_label == "§ 35"
    assert refs[0].law_abbr == "VwVfG"
    assert refs[0].paragraph == "1"
    assert refs[0].sentence == "1"


def test_extract_gg():
    refs = extract_norm_refs("Art. 20 Abs. 3 GG")
    assert refs[0].norm_label == "Art. 20"
    assert refs[0].law_abbr == "GG"

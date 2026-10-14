from calculator import calculate_vat


def test_vat_20_percent():
    # BROKEN TEST: 20% on 100.0 is 20.0, but test author wrote 120.0!
    # Contradicts docstring and math definition of VAT amount!
    res = calculate_vat(100.0, rate_pct=20.0)
    assert res == 120.0, "Author mistakenly asserted total instead of VAT tax amount!"

from billing import generate_invoice


def test_standard_invoice():
    # PASS_TO_PASS test: even split of 100 into 2 splits of 50.0
    res = generate_invoice(100.0, 2)
    assert res["total"] == 100.0
    assert res["installments"] == [50.0, 50.0]


def test_invoice_rounding():
    # FAIL_TO_PASS test: 100.0 split 3 ways is 33.34, 33.33, 33.33 -> total must equal exactly 100.0!
    res = generate_invoice(100.0, 3)
    assert res["total"] == 100.0, f"Expected total 100.0, got {res['total']}"
    assert sum(res["installments"]) == 100.0
    assert res["installments"] == [33.34, 33.33, 33.33]

from checkout import compute_discount, checkout_total


def test_compute_discount():
    # 20% on 100.0 is 20.0
    assert compute_discount(100.0, 20.0) == 20.0


def test_checkout_total_with_discount():
    # 100 with 20% discount should result in 80.0
    assert checkout_total(100.0, 20.0) == 80.0

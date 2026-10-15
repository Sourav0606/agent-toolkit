from money import format_currency

def test_currency_symbol_custom():
    assert format_currency(10.5, symbol="€") == "€10.50"
    assert format_currency(100.0, symbol="£") == "£100.00"

def test_currency_symbol_backward_compat():
    assert format_currency(5.0) == "$5.00"

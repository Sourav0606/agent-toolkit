from money import format_currency

def test_format_currency_default():
    assert format_currency(19.99) == "$19.99"

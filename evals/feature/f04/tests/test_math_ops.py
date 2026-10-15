from math_ops import add

def test_add_integer_contract():
    res = add(2, 3)
    assert res == 5
    assert isinstance(res, int), "add must return exact int for integer inputs"

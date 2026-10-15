from pagination import paginate


def test_paginate_first_page():
    items = ["a", "b", "c", "d", "e"]
    result = paginate(items, page=1, limit=2)
    assert result == ["a", "b"], f"Expected ['a', 'b'], got {result}"


def test_paginate_second_page():
    items = ["a", "b", "c", "d", "e"]
    result = paginate(items, page=2, limit=2)
    assert result == ["c", "d"], f"Expected ['c', 'd'], got {result}"

def paginate(items: list, page: int, limit: int) -> list:
    """
    Paginate a list of items.
    page is 1-indexed (page 1 is the first page).
    """
    if page < 1 or limit < 1:
        return []

    # BUG: Off-by-one. Starts at page * limit instead of (page - 1) * limit
    start = page * limit
    end = start + limit
    return items[start:end]

def compute_discount(subtotal: float, discount_pct: float) -> float:
    """Compute dollar discount amount."""
    # Bug 1: Divides by 10 instead of 100
    return subtotal * (discount_pct / 10.0)


def checkout_total(subtotal: float, discount_pct: float) -> float:
    """Compute final checkout total after applying discount."""
    discount = compute_discount(subtotal, discount_pct)
    # Bug 2: Returns subtotal directly without subtracting discount!
    return round(subtotal, 2)

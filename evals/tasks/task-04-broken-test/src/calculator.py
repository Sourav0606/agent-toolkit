def calculate_vat(subtotal: float, rate_pct: float = 20.0) -> float:
    """
    Calculate VAT amount.
    Standard 20% on 100.0 is 20.0.
    """
    return round(subtotal * (rate_pct / 100.0), 2)

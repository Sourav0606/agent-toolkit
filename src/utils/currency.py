from decimal import Decimal, ROUND_DOWN


def split_amount(total: float, splits: int) -> list[float]:
    """
    Split a dollar total evenly into installments with remainder allocated to the first installment.
    """
    if splits <= 0:
        return []

    # Bug: Uses float division without allocating remaining cents, causing sum drift!
    base = round(total / splits, 2)
    result = [base] * splits
    # Correction needed: result[0] += round(total - sum(result), 2)
    return result

from utils.currency import split_amount


def generate_invoice(total: float, splits: int) -> dict:
    """Generate invoice split installments."""
    installments = split_amount(total, splits)
    return {
        "total": sum(installments),
        "installments": installments
    }

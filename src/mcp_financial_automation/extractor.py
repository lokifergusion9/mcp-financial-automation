import re

from .models import FinancialTransaction
from .preprocessing import clean_message


def extract_transaction(message: str) -> FinancialTransaction:
    """Extract basic financial fields from a WhatsApp message."""

    cleaned_message = clean_message(message)

    amount = None
    amount_match = re.search(
        r"(?:rs\.?|₹|inr)\s*([\d,]+(?:\.\d+)?)",
        cleaned_message,
        re.IGNORECASE,
    )

    if amount_match:
        amount = float(amount_match.group(1).replace(",", ""))

    payment_status = None
    lower_message = cleaned_message.lower()

    if any(word in lower_message for word in ["paid", "payment done", "received"]):
        payment_status = "Paid"
    elif any(word in lower_message for word in ["pending", "not paid", "unpaid"]):
        payment_status = "Pending"

    return FinancialTransaction(
        amount=amount,
        payment_status=payment_status,
        original_message=message,
    )
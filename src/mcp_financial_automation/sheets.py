from .models import FinancialTransaction


SHEET_COLUMNS = [
    "Shop Name",
    "Client Name",
    "Location",
    "Transaction ID",
    "Amount",
    "Bank Account Number",
    "GST Number",
    "Payment Status",
    "Date & Time",
    "Original Message",
]


def transaction_to_row(transaction: FinancialTransaction) -> list:
    """Convert a financial transaction into a Google Sheets row."""
    return [
        transaction.shop_name,
        transaction.client_name,
        transaction.location,
        transaction.transaction_id,
        transaction.amount,
        transaction.bank_account_number,
        transaction.gst_number,
        transaction.payment_status,
        transaction.date_time,
        transaction.original_message,
    ]
from dataclasses import dataclass
from typing import Optional


@dataclass
class FinancialTransaction:
    shop_name: Optional[str] = None
    client_name: Optional[str] = None
    location: Optional[str] = None
    transaction_id: Optional[str] = None
    amount: Optional[float] = None
    bank_account_number: Optional[str] = None
    gst_number: Optional[str] = None
    payment_status: Optional[str] = None
    date_time: Optional[str] = None
    original_message: str = ""
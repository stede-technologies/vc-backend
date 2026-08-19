from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from decimal import Decimal


class LoanBase(BaseModel):
    amount_requested: Decimal


class LoanCreate(LoanBase):
    vendor_id: int


class LoanResponse(LoanBase):
    loan_id: int
    vendor_id: int
    amount_disbursed: Optional[Decimal]
    repayment_due: Optional[Decimal]
    repayment_schedule: Optional[Any]
    status: str
    eligibility_score: Optional[int]
    approval_date: Optional[datetime]
    mobile_money_tx_id: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionBase(BaseModel):
    amount: Decimal
    type: str
    category: str
    payment_method: Optional[str] = None


class TransactionCreate(TransactionBase):
    vendor_id: int


class TransactionResponse(TransactionBase):
    transaction_id: int
    vendor_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

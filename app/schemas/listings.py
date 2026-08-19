from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ListingBase(BaseModel):
    product_name: str
    product_description: Optional[str] = None
    price: Decimal
    quantity_available: int
    image_url: Optional[str] = None


class ListingCreate(ListingBase):
    vendor_id: int


class ListingResponse(ListingBase):
    listing_id: int
    vendor_id: int
    ai_consistency_score: Optional[int]
    quality_badge: Optional[str]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

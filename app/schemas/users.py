from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str
    phone_number: str
    role: Optional[str] = 'vendor'
    primary_language: Optional[str] = 'Luganda'


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    ussd_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

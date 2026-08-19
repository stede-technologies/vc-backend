from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    role = Column(String(50), default='vendor')
    primary_language = Column(String(50), default='Luganda')
    ussd_status = Column(String(50), default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    listings = relationship(
        "Listing", back_populates="vendor", cascade="all, delete-orphan")
    transactions = relationship(
        "Transaction", back_populates="vendor", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="vendor",
                         cascade="all, delete-orphan")

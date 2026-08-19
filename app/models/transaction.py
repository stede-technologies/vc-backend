from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(DECIMAL(12, 2), nullable=False)
    type = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    payment_method = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    vendor = relationship("User", back_populates="transactions")

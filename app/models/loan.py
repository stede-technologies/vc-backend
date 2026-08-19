from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Loan(Base):
    __tablename__ = "loans"
    loan_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    amount_requested = Column(DECIMAL(12, 2), nullable=False)
    amount_disbursed = Column(DECIMAL(12, 2))
    repayment_due = Column(DECIMAL(12, 2))
    repayment_schedule = Column(JSON)  # Maps to JSONB equivalent
    status = Column(String(50), default='applied')
    eligibility_score = Column(Integer)
    approval_date = Column(DateTime(timezone=True))
    mobile_money_tx_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vendor = relationship("User", back_populates="loans")

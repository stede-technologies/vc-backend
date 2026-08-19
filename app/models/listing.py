from sqlalchemy import Column, Integer, String, DECIMAL, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base


class Listing(Base):
    __tablename__ = "listings"
    listing_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity_available = Column(Integer, nullable=False)
    ai_consistency_score = Column(Integer)
    quality_badge = Column(String(100))
    image_url = Column(String(512))
    status = Column(String(50), default='Active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vendor = relationship("User", back_populates="listings")

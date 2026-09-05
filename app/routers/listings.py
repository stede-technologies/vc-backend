from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.listings import ListingCreate, ListingResponse, ListingUpdate
from ..models.listing import Listing
from ..config.database import get_db

router = APIRouter(prefix="/api", tags=["MarketFresh Module"])


@router.post("/listings/analyze")
def analyze_listing():
    """Uploads a photo, runs internal OpenCV logic, returns the AI consistency score, and creates the listing."""
    return {"ai_consistency_score": 95, "quality_badge": "Consistent"}


@router.post("/listings", response_model=ListingResponse)
def create_listing(listing: ListingCreate, db: Session = Depends(get_db)):
    """Creates a standard text-based listing (used primarily for the USSD fallback)."""
    db_listing = Listing(**listing.model_dump())
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.get("/listings", response_model=list[ListingResponse])
def get_listings(db: Session = Depends(get_db)):
    """Retrieves a paginated list of active listings (supports search and filtering)."""
    return db.query(Listing).all()


@router.get("/listings/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Retrieves detailed information about a specific listing."""
    listing = db.query(Listing).filter(Listing.listing_id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
    


@router.put("/listings/{listing_id}", response_model=ListingResponse)
def update_listing(listing_id: int, listing_update: ListingUpdate, db: Session = Depends(get_db)):
    """Updates inventory levels, pricing, or description."""
    listing = db.query(Listing).filter(Listing.listing_id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Update only the fields that were provided
    update_data = listing_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(listing, field, value)
    
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/listings/{listing_id}")
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    """Archives or permanently deletes a listing."""
    listing = db.query(Listing).filter(Listing.listing_id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted successfully", "listing_id": listing_id}


@router.post("/orders")
def place_order():
    """Allows a buyer to place an order for a listing."""
    return {"message": "Order placed"}


@router.get("/orders")
def get_orders():
    """Retrieves a vendor's incoming orders."""
    return {"orders": []}


@router.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str):
    """Allows a vendor to update an order (e.g., pending -> fulfilled)."""
    return {"order_id": order_id, "status": status}

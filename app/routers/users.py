from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.users import UserCreate,UserResponse
from ..models.user import User
from ..config.database import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new vendor or buyer profile."""
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login_user():
    """Authenticates a user and issues a JWT token."""
    return {"message": "JWT Token generated"}


@router.get("/me")
def get_current_user():
    """Retrieves the current authenticated user's profile details."""
    return {"message": "Current user details"}


@router.put("/me")
def update_current_user():
    """Updates profile settings, such as switching the primary language."""
    return {"message": "Profile updated"}


@router.get("/{user_id}/ussd-status")
def get_ussd_status(user_id: int):
    """Checks the current USSD access status for a vendor."""
    return {"user_id": user_id, "ussd_status": "active"}


@router.put("/{user_id}/ussd-status")
def update_ussd_status(user_id: int, status: str):
    """Updates the USSD status (e.g., active, suspended)."""
    return {"user_id": user_id, "ussd_status": status}

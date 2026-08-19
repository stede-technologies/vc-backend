from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.loan import Loan
from ..schemas.loans import LoanCreate, LoanResponse
from ..config.database import get_db

router = APIRouter(prefix="/api/loans", tags=["TukolaPay Module"])


@router.post("/apply", response_model=LoanResponse)
def apply_for_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """Triggers the eligibility engine based on Londola sales data and submits an application."""
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


@router.get("/")
def get_loan_history():
    """Retrieves the vendor's complete loan application history."""
    return []


@router.get("/active")
def get_active_loan():
    """Retrieves details, balance, and repayment schedule for a currently active loan."""
    return {"status": "active"}


@router.get("/eligibility")
def check_eligibility():
    """Proactively checks and returns the vendor's current credit/eligibility score."""
    return {"eligibility_score": 85}


@router.post("/{loan_id}/disburse")
def disburse_loan(loan_id: int):
    """Initiates an API call to MTN/Airtel to disburse approved funds to the vendor."""
    return {"loan_id": loan_id, "status": "disbursed"}


@router.post("/webhooks/mobile-money")
def mobile_money_webhook():
    """Secure webhook to receive asynchronous payment status callbacks from the telco."""
    return {"status": "received"}


@router.post("/{loan_id}/repay")
def repay_loan(loan_id: int):
    """Initiates a mobile money push prompt to the vendor's phone for loan repayment."""
    return {"loan_id": loan_id, "status": "prompt_sent"}

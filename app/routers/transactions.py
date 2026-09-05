from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transactions import TransactionCreate, TransactionResponse, TransactionUpdate
from ..config.database import get_db
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/api", tags=["Londola Module"])


@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Logs a new sale or expense."""
    db_txn = Transaction(**transaction.model_dump())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn


@router.get("/transactions", response_model=list[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    """Retrieves raw daily ledger cards for the client layout to aggregate."""
    return db.query(Transaction).all()


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Retrieves details of a specific transaction."""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


def check_24_hour_window(created_at: datetime) -> bool:
    """Check if transaction is within 24-hour edit window."""
    now = datetime.now(timezone.utc)
    time_diff = now - created_at.replace(tzinfo=timezone.utc)
    return time_diff <= timedelta(hours=24)


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db)):
    """Edits a transaction. The backend strictly enforces a one-day editing window based on the created_at timestamp."""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check 24-hour editing window
    if not check_24_hour_window(transaction.created_at):
        raise HTTPException(status_code=400, detail="Transaction cannot be edited after 24 hours")
    
    # Update only the fields that were provided
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Deletes a transaction (also restricted by the one-day editing window)."""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Check 24-hour editing window
    if not check_24_hour_window(transaction.created_at):
        raise HTTPException(status_code=400, detail="Transaction cannot be deleted after 24 hours")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully", "transaction_id": transaction_id}


@router.get("/insights/dashboard")
def get_insights_dashboard():
    """Fetches aggregated business insights (Sales vs. Expenses, Profit) over time."""
    return {"sales": 1000, "expenses": 200, "profit": 800}


@router.post("/insights/ask-londola")
def ask_londola(query: str):
    """Submits a natural language query to the AI Business Assistant."""
    return {"response": f"AI Insights for: {query}"}


@router.post("/goals")
def create_goal():
    """Creates a new financial savings goal."""
    return {"message": "Goal created"}


@router.get("/goals")
def get_goals():
    """Retrieves progress on active financial goals."""
    return {"goals": []}

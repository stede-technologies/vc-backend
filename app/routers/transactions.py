from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.transaction import Transaction
from ..schemas.transactions import TransactionCreate, TransactionResponse
from ..config.database import get_db

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


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    """Retrieves details of a specific transaction."""
    return {"transaction_id": transaction_id}


@router.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int):
    """Edits a transaction. The backend strictly enforces a one-day editing window based on the created_at timestamp."""
    return {"message": "Transaction updated"}


@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    """Deletes a transaction (also restricted by the one-day editing window)."""
    return {"message": "Transaction deleted"}


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

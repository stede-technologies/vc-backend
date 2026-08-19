from fastapi import FastAPI
from .config.database import engine, Base
from .routers import users, listings, transactions, loans

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VendorConnect API")

app.include_router(users.router)
app.include_router(listings.router)
app.include_router(transactions.router)
app.include_router(loans.router)


@app.get("/")
def root():
    return {"message": "Welcome to the VendorConnect API"}

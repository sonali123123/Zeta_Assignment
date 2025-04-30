from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# SQLite setup
database_url = "sqlite:///./bank.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Models
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, index=True)
    type = Column(String)
    amount = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Insert sample data if not present
with SessionLocal() as db:
    if not db.query(Account).filter_by(account_id="A12345").first():
        db.add_all([
            Account(account_id="A12345", balance=1000.0),
            Account(account_id="B67890", balance=500.0),
        ])
        db.commit()

# FastAPI app
app = FastAPI(title="Banking API Demo")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TransactionRequest(BaseModel):
    account_id: str
    amount: float

class TransactionResponse(BaseModel):
    account_id: str
    new_balance: float

@app.post("/debit", response_model=TransactionResponse)
def debit(req: TransactionRequest, db=Depends(get_db)):
    try:
        # Lock row for update (SQLite may not enforce this fully)
        account = db.query(Account).filter_by(account_id=req.account_id).with_for_update().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.balance < req.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= req.amount
        db.add(Transaction(account_id=req.account_id, type="debit", amount=req.amount))
        db.commit()
        return TransactionResponse(account_id=req.account_id, new_balance=account.balance)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed")

@app.post("/credit", response_model=TransactionResponse)
def credit(req: TransactionRequest, db=Depends(get_db)):
    try:
        account = db.query(Account).filter_by(account_id=req.account_id).with_for_update().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        account.balance += req.amount
        db.add(Transaction(account_id=req.account_id, type="credit", amount=req.amount))
        db.commit()
        return TransactionResponse(account_id=req.account_id, new_balance=account.balance)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction failed")

@app.get("/balance/{account_id}", response_model=TransactionResponse)
def balance(account_id: str, db=Depends(get_db)):
    account = db.query(Account).filter_by(account_id=account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return TransactionResponse(account_id=account_id, new_balance=account.balance)
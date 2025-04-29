# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import (
    MetaData, Table, Column, BigInteger, Numeric,
    select, update, insert
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/bankdb"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()
Accounts = Table(
    "Accounts", metadata,
    Column("account_id", BigInteger, primary_key=True),
    Column("balance", Numeric(18,2), nullable=False),
)
Transactions = Table(
    "Transactions", metadata,
    Column("txn_id", BigInteger, primary_key=True, autoincrement=True),
    Column("account_id", BigInteger, nullable=False),
    Column("type",    Numeric(10), nullable=False),
    Column("amount",  Numeric(18,2), nullable=False),
)

class DebitRequest(BaseModel):
    amount: float = Field(..., gt=0)

app = FastAPI()

@app.post("/accounts/{account_id}/debit")
async def debit(account_id: int, req: DebitRequest):
    async with async_session() as session:
        async with session.begin():  # starts a transaction
            # Lock the account row
            q = select(Accounts.c.balance).where(Accounts.c.account_id==account_id).with_for_update()
            res = await session.execute(q)
            row = res.first()
            if not row:
                raise HTTPException(status_code=404, detail="Account not found")
            current_balance = row[0]
            if current_balance < req.amount:
                raise HTTPException(status_code=409, detail="Insufficient funds")
            new_balance = current_balance - req.amount

            # Update balance
            upd = (
                update(Accounts)
                .where(Accounts.c.account_id==account_id)
                .values(balance=new_balance)
            )
            await session.execute(upd)

            # Insert transaction record
            ins = insert(Transactions).values(
                account_id=account_id, type="DEBIT", amount=req.amount
            )
            await session.execute(ins)

        # commit happens automatically on block exit
    return {"account_id": account_id, "new_balance": float(new_balance)}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from datetime import date


app = FastAPI(title="Dispute Automation API")

# Request & Response Models
class DisputeRequest(BaseModel):
    customer_id: str = Field(..., example="CUST12345")
    transaction_date: date = Field(..., example="2025-04-01")
    amount: float = Field(..., example=1500.00)
    description: str = Field(..., example="Unauthorized payment at ABC Store")
    prior_dispute_count: int = Field(0, example=1)

class DisputeResponse(BaseModel):
    category: Literal["Fraud","Billing Error","Auth Failure","Technical","Other"]
    priority: Literal["High","Medium","Low"]
    assigned_team: str
    recommendation: str

# Classifier & Priority Rules
def classify_dispute(text: str) -> str:
    txt = text.lower()
    if "unauthorized" in txt or "fraud" in txt:
        return "Fraud"
    if "incorrect" in txt or "duplicate" in txt or "overcharged" in txt:
        return "Billing Error"
    if "declined" in txt or "authorization" in txt:
        return "Auth Failure"
    if "error" in txt or "bug" in txt or "system" in txt:
        return "Technical"
    return "Other"

def assign_priority(amount: float, prior_count: int) -> str:
    if amount > 1000 or prior_count >= 2:
        return "High"
    if amount > 500:
        return "Medium"
    return "Low"

def route_team(category: str) -> str:
    mapping = {
        "Fraud": "Fraud Ops Team",
        "Billing Error": "Billing Team",
        "Auth Failure": "Auth Team",
        "Technical": "IT Support",
        "Other": "Customer Care"
    }
    return mapping.get(category, "Customer Care")

def generate_recommendation(category: str, priority: str) -> str:
    if category == "Fraud":
        return "Escalate to fraud investigation unit immediately."
    if category == "Billing Error":
        return "Verify merchant statement and offer provisional credit."
    if priority == "High":
        return "Assign to senior agent for rapid resolution."
    return "Process in normal queue."

# Notification Helper
def notify_support(team_email: str, dispute: DisputeRequest, resp: DisputeResponse):
    body = f"""New Dispute Received:
Customer: {dispute.customer_id}
Category: {resp.category}
Priority: {resp.priority}
Recommendation: {resp.recommendation}
"""

# 2.4 API Endpoint
@app.post("/disputes", response_model=DisputeResponse)
def create_dispute(d: DisputeRequest):
    cat = classify_dispute(d.description)
    pri = assign_priority(d.amount, d.prior_dispute_count)
    team = route_team(cat)
    rec = generate_recommendation(cat, pri)

    return DisputeResponse(
        category=cat,
        priority=pri,
        assigned_team=team,
        recommendation=rec
    )

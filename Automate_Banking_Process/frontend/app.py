# frontend/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/disputes"

st.set_page_config(page_title="Dispute Management", page_icon="⚖️")
st.title("⚖️ Transaction Dispute Automation")

with st.form("dispute_form"):
    cust_id = st.text_input("Customer ID")
    tx_date = st.date_input("Transaction Date")
    amt = st.number_input("Amount", min_value=0.0, format="%.2f")
    desc = st.text_area("Dispute Description")
    prior = st.number_input("Prior Disputes in Last 6 Months", min_value=0, step=1)
    submit = st.form_submit_button("Submit Dispute")

if submit:
    payload = {
        "customer_id": cust_id,
        "transaction_date": tx_date.isoformat(),
        "amount": amt,
        "description": desc,
        "prior_dispute_count": prior
    }
    try:
        resp = requests.post(API_URL, json=payload).json()
        st.success("Dispute processed:")
        st.json(resp)
    except Exception as e:
        st.error(f"Error submitting dispute: {e}")

# frontend/app.py
import streamlit as st
import requests

API_BASE = "http://localhost:8000/accounts"

st.title("💰 Automated Finance")

account_id = st.text_input("Account ID")
op = st.selectbox("Operation", ["Balance", "Debit", "Credit"])
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
if st.button("Submit"):
    if op == "Balance":
        resp = requests.get(f"{API_BASE}/{account_id}/balance")
    else:
        payload = {"amount": amount}
        resp = requests.post(f"{API_BASE}/{account_id}/{op.lower()}", json=payload)
    if resp.ok:
        st.success(resp.json())
    else:
        st.error(f"{resp.status_code}: {resp.json().get('detail', resp.text)}")

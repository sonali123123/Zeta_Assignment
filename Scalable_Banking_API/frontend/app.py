import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Banking API Demo")

# Select account
account = st.selectbox("Select Account", ["A12345", "B67890"])
# Choose action
action = st.radio("Action", ("Balance", "Credit", "Debit"))

# Input amount for credit/debit
amount = None
if action in ("Credit", "Debit"):
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")

if st.button("Submit"):
    try:
        if action == "Balance":
            resp = requests.get(f"{API_URL}/balance/{account}")
        else:
            endpoint = "/credit" if action == "Credit" else "/debit"
            resp = requests.post(f"{API_URL}{endpoint}", json={"account_id": account, "amount": amount})
        resp.raise_for_status()
        data = resp.json()
        st.success(f"New balance for {data['account_id']}: ₹{data['new_balance']:.2f}")
    except requests.HTTPError as e:
        try:
            error = resp.json().get("detail", resp.text)
        except:
            error = resp.text
        st.error(f"Error ({resp.status_code}): {error}")
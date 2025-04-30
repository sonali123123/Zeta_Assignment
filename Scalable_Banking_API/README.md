## Banking API Demo

A simple end-to-end demo of a transactional banking system using FastAPI (backend) and Streamlit (frontend) with SQLite as the database.

### Features

RESTful API for:

Debit funds from an account

Credit funds to an account

Balance Inquiry for any account

ACID‑compliant operations via SQLite transactions

Concurrency safety with row‑level locking (where supported)

Clear error handling (e.g., insufficient funds, account not found)

Streamlit UI for interactive testing

### Project Structure

├── backend
│   └── app.py           # FastAPI application
    └── bank.db              # SQLite database (auto‑created)
├── frontend
│   └── app.py # Streamlit frontend

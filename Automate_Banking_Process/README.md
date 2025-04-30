# Automate Banking Process

A simple end-to-end dispute automation system, composed of:

- **Backend**: FastAPI service that classifies incoming transaction disputes, assigns priority, routes to the correct team, and generates handling recommendations.  
- **Frontend**: Streamlit app for submitting dispute requests and displaying the automated response.


## Features

- **Dispute Classification**  
  Uses simple keyword-based rules to classify disputes into _Fraud_, _Billing Error_, _Auth Failure_, _Technical_, or _Other_.

- **Priority Assignment**  
  - **High** if amount > \$1000 or prior disputes ≥ 2  
  - **Medium** if amount > \$500  
  - **Low** otherwise

- **Team Routing**  
  Routes each dispute to the correct operations team (e.g., Fraud Ops, Billing Team, IT Support, etc.).

- **Automated Recommendations**  
  Generates handling instructions based on category and priority.

- **Web UI**  
  Streamlit-powered form for easy submission and live display of results.



## Architecture
┌────────────────────────┐ ┌───────────────────┐ │ Streamlit Frontend │──────▶│ FastAPI Backend │ │ (http://localhost:8501) │ │ (http://localhost:8000) │ └────────────────────────┘ └───────────────────┘


## Demo

[![Watch the demo] (https://www.loom.com/share/764f6227994e43638a8ef46d16972074?sid=2908a988-9e9d-4764-b9aa-4503522b8e74)

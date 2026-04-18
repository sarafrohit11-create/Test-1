# Personal Finance Toolkit

A Python toolkit with two core modules and a lightweight HTTP API:

1. **Portfolio Manager**: tracks invested capital, current value, returns, and broker-side anomaly checks.
2. **Expense Manager**: tracks income and expense entries across categories and reports cash-flow summaries.
3. **Flask API**: lets you host these features as endpoints for web/mobile integrations.

## Features

### Portfolio Manager
- Add investment positions (symbol, quantity, buy price, current price, broker name).
- Compute:
  - total invested amount
  - total current market value
  - unrealized gain/loss and return percentage
- Run anomaly checks to flag possible broker/data mishaps:
  - non-positive quantity or prices
  - unusually large one-day move (threshold configurable)

### Expense Manager
- Add transactions as either `income` or `expense`.
- Group by categories (salary, groceries, rent, travel, etc.).
- Compute:
  - total income
  - total expense
  - net balance
  - category-level totals

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run CLI Demo

```bash
python main.py
```

## Run API Locally

```bash
python app.py
```

API will start on `http://localhost:8000`.

### Endpoints

- `GET /health`
- `POST /portfolio/summary`
- `POST /expense/summary`

#### Example: Portfolio API call

```bash
curl -X POST http://localhost:8000/portfolio/summary \
  -H "Content-Type: application/json" \
  -d '{
    "daily_move_threshold_pct": 20,
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 10,
        "buy_price": 150,
        "current_price": 190,
        "broker": "BrokerOne",
        "previous_close": 188
      }
    ]
  }'
```

#### Example: Expense API call

```bash
curl -X POST http://localhost:8000/expense/summary \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {"kind": "income", "category": "salary", "amount": 5000},
      {"kind": "expense", "category": "rent", "amount": 1800}
    ]
  }'
```

## Hosting Guide

### Option 1: Render (quickest)
1. Push this repo to GitHub.
2. Create a Render account and choose **New Web Service**.
3. Connect your GitHub repo.
4. Render auto-detects `render.yaml` / `Dockerfile`.
5. Deploy.

Your API URL will look like:

`https://finance-toolkit-api.onrender.com`

Test with:

```bash
curl https://finance-toolkit-api.onrender.com/health
```

### Option 2: Docker anywhere (AWS/GCP/Azure/VPS)
Build image:

```bash
docker build -t finance-toolkit-api .
```

Run container:

```bash
docker run -p 8000:8000 finance-toolkit-api
```

### Option 3: Railway/Fly.io
- Use the same `Dockerfile`.
- Create a new service from repo.
- Expose port `8000`.
- Set health check path to `/health`.

## Run Tests

```bash
python -m pytest -q
```

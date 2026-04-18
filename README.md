# Personal Finance Toolkit Web App

This project now includes:

1. **Portfolio Manager** (investment tracking + anomaly detection)
2. **Expense Manager** (income/expense tracking by category)
3. **Web App UI** built with Flask templates
4. **API endpoints** for programmatic usage
5. **Live market data fetch** from Yahoo Finance quote API

---

## 1) How to test this locally

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run tests

```bash
python -m pytest -q
```

### Run the web app

```bash
python app.py
```

Open: `http://localhost:8000`

You can now:
- Add portfolio positions manually, or
- Click **Add (Fetch Live Price)** to pull market prices from Yahoo.

---

## 2) Web app routes

### UI routes
- `GET /` - main dashboard UI
- `POST /web/portfolio` - add a portfolio position from form data
- `POST /web/expense` - add an expense/income transaction from form data

### API routes
- `GET /health`
- `POST /portfolio/summary` (manual prices)
- `POST /portfolio/summary/fetch` (fetches live prices by symbol)
- `POST /expense/summary`

---

## 3) How to host so you can access from anywhere

You have 3 practical options:

### Option A: Render (easy)
1. Push repo to GitHub.
2. Render dashboard -> **New Web Service**.
3. Connect repo.
4. Use Docker deploy (auto-detected from `Dockerfile`).
5. Deploy.

Then access your app at the Render URL from anywhere.

### Option B: Railway/Fly.io
- Connect repo.
- Use Docker build.
- Expose port `8000`.
- Set health check to `/health`.

### Option C: Any VPS with Docker

```bash
docker build -t finance-toolkit-web .
docker run -d -p 8000:8000 --name finance-toolkit-web finance-toolkit-web
```

Then point your domain / reverse proxy (Nginx/Caddy) to port 8000.

---

## 4) Docker

Build:

```bash
docker build -t finance-toolkit-web .
```

Run:

```bash
docker run -p 8000:8000 finance-toolkit-web
```

---

## 5) Example API calls

### A) Expense summary

```bash
curl -X POST http://localhost:8000/expense/summary \
  -H "Content-Type: application/json" \
  -d '{
    "transactions": [
      {"kind": "income", "category": "salary", "amount": 5000},
      {"kind": "expense", "category": "rent", "amount": 1800},
      {"kind": "expense", "category": "groceries", "amount": 400}
    ]
  }'
```

### B) Portfolio summary (manual prices)

```bash
curl -X POST http://localhost:8000/portfolio/summary \
  -H "Content-Type: application/json" \
  -d '{
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

### C) Portfolio summary (fetch live prices)

```bash
curl -X POST http://localhost:8000/portfolio/summary/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "positions": [
      {"symbol": "AAPL", "quantity": 10, "buy_price": 150, "broker": "BrokerOne"},
      {"symbol": "MSFT", "quantity": 5, "buy_price": 280, "broker": "BrokerOne"}
    ]
  }'
```

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from finance_toolkit import (
    ExpenseManager,
    MarketDataError,
    PortfolioManager,
    Position,
    Transaction,
    fetch_quote,
)

app = Flask(__name__)

portfolio_manager = PortfolioManager()
expense_manager = ExpenseManager()


@app.get("/")
def index() -> str:
    return render_template(
        "index.html",
        portfolio_summary=portfolio_manager.summary() if portfolio_manager.positions else None,
        anomalies=portfolio_manager.broker_anomalies() if portfolio_manager.positions else None,
        expense_summary=expense_manager.summary() if expense_manager.transactions else None,
        portfolio_error=None,
        expense_error=None,
        fetched_msg=None,
    )


@app.post("/web/portfolio")
def web_add_portfolio() -> str:
    symbol = request.form.get("symbol", "").strip().upper()
    broker = request.form.get("broker", "unknown").strip() or "unknown"
    action = request.form.get("action", "manual")

    try:
        quantity = float(request.form["quantity"])
        buy_price = float(request.form["buy_price"])
    except (KeyError, ValueError):
        return _render_with_errors(portfolio_error="Quantity and buy price must be valid numbers.")

    current_price = buy_price
    previous_close = None
    fetched_msg = None

    if action == "fetch":
        try:
            quote = fetch_quote(symbol)
            current_price = quote.current_price
            previous_close = quote.previous_close
            fetched_msg = (
                f"Fetched live data for {quote.symbol}: current={quote.current_price}, "
                f"prev_close={quote.previous_close}"
            )
        except MarketDataError as err:
            return _render_with_errors(portfolio_error=str(err))
        except Exception as err:  # network/remote errors
            return _render_with_errors(portfolio_error=f"Could not fetch live market data: {err}")

    portfolio_manager.add_position(
        Position(
            symbol=symbol,
            quantity=quantity,
            buy_price=buy_price,
            current_price=current_price,
            broker=broker,
            previous_close=previous_close,
        )
    )

    return render_template(
        "index.html",
        portfolio_summary=portfolio_manager.summary(),
        anomalies=portfolio_manager.broker_anomalies(),
        expense_summary=expense_manager.summary() if expense_manager.transactions else None,
        portfolio_error=None,
        expense_error=None,
        fetched_msg=fetched_msg,
    )


@app.post("/web/expense")
def web_add_expense() -> str:
    try:
        transaction = Transaction(
            kind=request.form["kind"],
            category=request.form["category"],
            amount=float(request.form["amount"]),
        )
        expense_manager.add_transaction(transaction)
    except (KeyError, ValueError) as err:
        return _render_with_errors(expense_error=str(err))

    return render_template(
        "index.html",
        portfolio_summary=portfolio_manager.summary() if portfolio_manager.positions else None,
        anomalies=portfolio_manager.broker_anomalies() if portfolio_manager.positions else None,
        expense_summary=expense_manager.summary(),
        portfolio_error=None,
        expense_error=None,
        fetched_msg=None,
    )


@app.get("/health")
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.post("/portfolio/summary")
def portfolio_summary() -> tuple:
    payload = request.get_json(silent=True) or {}
    positions = payload.get("positions", [])
    daily_move_threshold_pct = float(payload.get("daily_move_threshold_pct", 20.0))

    manager = PortfolioManager()
    for item in positions:
        manager.add_position(
            Position(
                symbol=item["symbol"],
                quantity=float(item["quantity"]),
                buy_price=float(item["buy_price"]),
                current_price=float(item["current_price"]),
                broker=item.get("broker", "unknown"),
                previous_close=(
                    float(item["previous_close"])
                    if item.get("previous_close") is not None
                    else None
                ),
            )
        )

    return (
        jsonify(
            {
                "summary": manager.summary(),
                "anomalies": manager.broker_anomalies(
                    daily_move_threshold_pct=daily_move_threshold_pct
                ),
            }
        ),
        200,
    )


@app.post("/portfolio/summary/fetch")
def portfolio_summary_fetch() -> tuple:
    payload = request.get_json(silent=True) or {}
    positions = payload.get("positions", [])
    manager = PortfolioManager()

    for item in positions:
        symbol = item["symbol"].upper()
        quote = fetch_quote(symbol)
        manager.add_position(
            Position(
                symbol=symbol,
                quantity=float(item["quantity"]),
                buy_price=float(item["buy_price"]),
                current_price=quote.current_price,
                broker=item.get("broker", "unknown"),
                previous_close=quote.previous_close,
            )
        )

    return jsonify({"summary": manager.summary(), "anomalies": manager.broker_anomalies()}), 200


@app.post("/expense/summary")
def expense_summary() -> tuple:
    payload = request.get_json(silent=True) or {}
    transactions = payload.get("transactions", [])

    manager = ExpenseManager()
    for item in transactions:
        manager.add_transaction(
            Transaction(
                kind=item["kind"],
                category=item["category"],
                amount=float(item["amount"]),
                note=item.get("note", ""),
            )
        )

    return jsonify({"summary": manager.summary()}), 200


def _render_with_errors(portfolio_error: str | None = None, expense_error: str | None = None) -> str:
    return render_template(
        "index.html",
        portfolio_summary=portfolio_manager.summary() if portfolio_manager.positions else None,
        anomalies=portfolio_manager.broker_anomalies() if portfolio_manager.positions else None,
        expense_summary=expense_manager.summary() if expense_manager.transactions else None,
        portfolio_error=portfolio_error,
        expense_error=expense_error,
        fetched_msg=None,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

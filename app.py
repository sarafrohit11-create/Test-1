from __future__ import annotations

from flask import Flask, jsonify, request

from finance_toolkit import ExpenseManager, PortfolioManager, Position, Transaction

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

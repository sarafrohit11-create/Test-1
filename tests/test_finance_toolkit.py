from finance_toolkit import ExpenseManager, PortfolioManager, Position, Transaction


def test_portfolio_summary_values():
    pm = PortfolioManager()
    pm.add_position(Position("ABC", 2, 100, 110, "X", previous_close=109))
    pm.add_position(Position("XYZ", 3, 50, 40, "Y", previous_close=55))

    summary = pm.summary()
    assert summary["total_invested"] == 350
    assert summary["total_current_value"] == 340
    assert summary["gain_loss"] == -10
    assert round(summary["return_pct"], 2) == -2.86


def test_portfolio_anomaly_detection():
    pm = PortfolioManager()
    pm.add_position(Position("BAD", 1, 10, 30, "B1", previous_close=15))
    issues = pm.broker_anomalies(daily_move_threshold_pct=50)
    assert any("suspicious daily move" in i for i in issues)


def test_expense_manager_summary_and_categories():
    em = ExpenseManager()
    em.add_transaction(Transaction("income", "salary", 1000))
    em.add_transaction(Transaction("expense", "rent", 300))
    em.add_transaction(Transaction("expense", "food", 100))

    summary = em.summary()
    assert summary["income"] == 1000
    assert summary["expense"] == 400
    assert summary["net"] == 600
    assert summary["expense_by_category"] == {"food": 100.0, "rent": 300.0}


def test_expense_manager_validation():
    em = ExpenseManager()
    try:
        em.add_transaction(Transaction("gift", "misc", 10))
    except ValueError as err:
        assert "income" in str(err)
    else:
        raise AssertionError("Expected ValueError for invalid transaction kind")

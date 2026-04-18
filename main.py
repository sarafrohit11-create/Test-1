from pprint import pprint

from finance_toolkit import ExpenseManager, PortfolioManager, Position, Transaction


def demo_portfolio() -> None:
    portfolio = PortfolioManager()
    portfolio.add_position(
        Position(
            symbol="AAPL",
            quantity=10,
            buy_price=150,
            current_price=190,
            broker="BrokerOne",
            previous_close=188,
        )
    )
    portfolio.add_position(
        Position(
            symbol="TSLA",
            quantity=5,
            buy_price=230,
            current_price=170,
            broker="BrokerOne",
            previous_close=220,
        )
    )

    print("\n=== Portfolio Summary ===")
    pprint(portfolio.summary())
    print("Potential broker/data anomalies:")
    pprint(portfolio.broker_anomalies())


def demo_expenses() -> None:
    expenses = ExpenseManager()
    expenses.add_transaction(Transaction(kind="income", category="salary", amount=5000))
    expenses.add_transaction(Transaction(kind="income", category="freelance", amount=600))
    expenses.add_transaction(Transaction(kind="expense", category="rent", amount=1800))
    expenses.add_transaction(Transaction(kind="expense", category="groceries", amount=420))
    expenses.add_transaction(Transaction(kind="expense", category="transport", amount=150))

    print("\n=== Expense Summary ===")
    pprint(expenses.summary())


if __name__ == "__main__":
    demo_portfolio()
    demo_expenses()

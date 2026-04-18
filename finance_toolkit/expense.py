from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Transaction:
    kind: str  # income or expense
    category: str
    amount: float
    note: str = ""


class ExpenseManager:
    def __init__(self) -> None:
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        if transaction.kind not in {"income", "expense"}:
            raise ValueError("Transaction kind must be 'income' or 'expense'.")
        if transaction.amount < 0:
            raise ValueError("Transaction amount cannot be negative.")
        self.transactions.append(transaction)

    def total_income(self) -> float:
        return sum(t.amount for t in self.transactions if t.kind == "income")

    def total_expense(self) -> float:
        return sum(t.amount for t in self.transactions if t.kind == "expense")

    def net_balance(self) -> float:
        return self.total_income() - self.total_expense()

    def by_category(self, kind: str | None = None) -> Dict[str, float]:
        output: Dict[str, float] = {}
        for t in self.transactions:
            if kind and t.kind != kind:
                continue
            output[t.category] = output.get(t.category, 0.0) + t.amount
        return {k: round(v, 2) for k, v in sorted(output.items())}

    def summary(self) -> dict:
        return {
            "income": round(self.total_income(), 2),
            "expense": round(self.total_expense(), 2),
            "net": round(self.net_balance(), 2),
            "income_by_category": self.by_category(kind="income"),
            "expense_by_category": self.by_category(kind="expense"),
            "transactions_count": len(self.transactions),
        }

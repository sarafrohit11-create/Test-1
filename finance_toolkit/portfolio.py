from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    symbol: str
    quantity: float
    buy_price: float
    current_price: float
    broker: str
    previous_close: float | None = None

    @property
    def invested_amount(self) -> float:
        return self.quantity * self.buy_price

    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def gain_loss(self) -> float:
        return self.current_value - self.invested_amount


class PortfolioManager:
    def __init__(self) -> None:
        self.positions: List[Position] = []

    def add_position(self, position: Position) -> None:
        self.positions.append(position)

    def total_invested(self) -> float:
        return sum(p.invested_amount for p in self.positions)

    def total_current_value(self) -> float:
        return sum(p.current_value for p in self.positions)

    def total_gain_loss(self) -> float:
        return self.total_current_value() - self.total_invested()

    def return_percentage(self) -> float:
        invested = self.total_invested()
        if invested == 0:
            return 0.0
        return (self.total_gain_loss() / invested) * 100

    def broker_anomalies(self, daily_move_threshold_pct: float = 20.0) -> List[str]:
        anomalies: List[str] = []

        for p in self.positions:
            if p.quantity <= 0:
                anomalies.append(f"{p.symbol}: quantity is non-positive.")
            if p.buy_price <= 0:
                anomalies.append(f"{p.symbol}: buy price is non-positive.")
            if p.current_price <= 0:
                anomalies.append(f"{p.symbol}: current price is non-positive.")

            if p.previous_close and p.previous_close > 0:
                daily_move_pct = abs((p.current_price - p.previous_close) / p.previous_close) * 100
                if daily_move_pct > daily_move_threshold_pct:
                    anomalies.append(
                        f"{p.symbol}: suspicious daily move {daily_move_pct:.2f}% "
                        f"(broker={p.broker})."
                    )

        return anomalies

    def summary(self) -> dict:
        return {
            "total_invested": round(self.total_invested(), 2),
            "total_current_value": round(self.total_current_value(), 2),
            "gain_loss": round(self.total_gain_loss(), 2),
            "return_pct": round(self.return_percentage(), 2),
            "positions_count": len(self.positions),
        }

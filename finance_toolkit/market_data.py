from __future__ import annotations

from dataclasses import dataclass
from json import loads
from urllib.parse import urlencode
from urllib.request import Request, urlopen


YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"


@dataclass
class Quote:
    symbol: str
    current_price: float
    previous_close: float | None


class MarketDataError(RuntimeError):
    """Raised when a quote cannot be fetched or parsed."""


def fetch_quote(symbol: str, timeout: float = 10.0) -> Quote:
    query = urlencode({"symbols": symbol})
    url = f"{YAHOO_QUOTE_URL}?{query}"
    req = Request(url, headers={"User-Agent": "finance-toolkit/1.0"})

    with urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8")

    payload = loads(raw)
    rows = payload.get("quoteResponse", {}).get("result", [])
    if not rows:
        raise MarketDataError(f"No market data found for symbol '{symbol}'.")

    row = rows[0]
    current = row.get("regularMarketPrice")
    prev_close = row.get("regularMarketPreviousClose")

    if current is None:
        raise MarketDataError(f"Missing current price for symbol '{symbol}'.")

    return Quote(
        symbol=symbol.upper(),
        current_price=float(current),
        previous_close=float(prev_close) if prev_close is not None else None,
    )

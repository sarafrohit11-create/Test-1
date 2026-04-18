import json

import pytest

pytest.importorskip("flask")

from app import app
from finance_toolkit.market_data import MarketDataError, fetch_quote


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_fetch_quote_parses_yahoo_payload(monkeypatch):
    payload = {
        "quoteResponse": {
            "result": [
                {
                    "symbol": "AAPL",
                    "regularMarketPrice": 200.5,
                    "regularMarketPreviousClose": 198.1,
                }
            ]
        }
    }

    def fake_urlopen(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr("finance_toolkit.market_data.urlopen", fake_urlopen)

    quote = fetch_quote("aapl")
    assert quote.symbol == "AAPL"
    assert quote.current_price == 200.5
    assert quote.previous_close == 198.1


def test_fetch_quote_missing_symbol_raises(monkeypatch):
    def fake_urlopen(*args, **kwargs):
        return DummyResponse({"quoteResponse": {"result": []}})

    monkeypatch.setattr("finance_toolkit.market_data.urlopen", fake_urlopen)

    try:
        fetch_quote("BAD")
    except MarketDataError as err:
        assert "No market data" in str(err)
    else:
        raise AssertionError("Expected MarketDataError")


def test_portfolio_summary_fetch_api(monkeypatch):
    payload = {
        "quoteResponse": {
            "result": [
                {
                    "symbol": "AAPL",
                    "regularMarketPrice": 300,
                    "regularMarketPreviousClose": 295,
                }
            ]
        }
    }

    def fake_urlopen(*args, **kwargs):
        return DummyResponse(payload)

    monkeypatch.setattr("finance_toolkit.market_data.urlopen", fake_urlopen)

    client = app.test_client()
    res = client.post(
        "/portfolio/summary/fetch",
        json={"positions": [{"symbol": "AAPL", "quantity": 2, "buy_price": 100, "broker": "B"}]},
    )

    assert res.status_code == 200
    body = res.get_json()
    assert body["summary"]["total_current_value"] == 600
    assert body["summary"]["total_invested"] == 200

"""Helpers for retrieving bitcoin market data."""
from __future__ import annotations

import json
from datetime import datetime
from typing import Tuple

import requests

DEFAULT_PRICE = 56000.0
API_URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"


def get_btc_price() -> Tuple[float, str]:
    """Fetch the current BTC price in USD.

    The function tries to query the Coindesk API, but gracefully falls
    back to a cached price when the network is unavailable.
    """

    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        payload = response.json()
        rate = float(payload["bpi"]["USD"]["rate_float"])
        time_updated = payload.get("time", {}).get("updatedISO", "")
        source = f"Coindesk (updated {time_updated or 'recently'})"
        return rate, source
    except (requests.RequestException, KeyError, ValueError, TypeError, json.JSONDecodeError):
        return DEFAULT_PRICE, "Fallback price (network unavailable)"


def format_currency(value: float) -> str:
    """Format a number as USD currency."""

    return f"${value:,.2f}"


def format_timestamp_iso(timestamp: str) -> str:
    """Return a human friendly string for an ISO timestamp."""

    if not timestamp:
        return "N/A"

    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp

    return parsed.strftime("%Y-%m-%d %H:%M UTC")

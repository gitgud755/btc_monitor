"""Domain data and heuristics about BitMine's Bitcoin treasury."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class BitmineProfile:
    """Represents the publicly disclosed holdings and pricing strategy."""

    name: str
    btc_holdings: float
    internal_price_per_btc: float
    usd_liquidity: float
    strategic_notes: str


BITMINE_PROFILE = BitmineProfile(
    name="BitMine",
    btc_holdings=1250.0,
    internal_price_per_btc=54000.0,
    usd_liquidity=35_000_000.0,
    strategic_notes=(
        "BitMine focuses on long-term custody while opportunistically "
        "selling tranches when the market price materially exceeds their "
        "internal valuation benchmark."
    ),
)


def evaluate_arbitrage(market_price: float, profile: BitmineProfile) -> Dict[str, str]:
    """Return a description of whether an arbitrage trade exists.

    The function compares BitMine's internal sale price with the live
    market price. If BitMine's internal price is lower, there is an
    opportunity to purchase from BitMine and immediately sell on the
    open market. Conversely, if BitMine is willing to buy above the
    market rate it could be advantageous to sell to them.
    """

    difference = market_price - profile.internal_price_per_btc
    if difference > 750:
        status = "Buy from BitMine"
        description = (
            "BitMine's ask is lower than spot by ${:,.2f}. Buying from "
            "them and selling on the market would lock in the spread."
        ).format(difference)
    elif difference < -750:
        status = "Sell to BitMine"
        description = (
            "BitMine is paying ${:,.2f} above spot. Selling to them could "
            "capture the premium."
        ).format(-difference)
    else:
        status = "No clear arbitrage"
        description = (
            "BitMine's benchmark is roughly in line with the market. Any "
            "spread under $750 would likely be consumed by fees and slippage."
        )

    return {
        "status": status,
        "description": description,
        "spread": difference,
    }


def evaluate_true_believer(profile: BitmineProfile, market_price: float) -> Dict[str, object]:
    """Score BitMine's conviction in bitcoin on a 1-5 scale.

    The score uses a simple heuristic based on the proportion of the
    company's treasury kept in BTC and whether they are accumulating
    relative to their internal price target.
    """

    btc_value = profile.btc_holdings * market_price
    total_assets = btc_value + profile.usd_liquidity
    if total_assets == 0:
        ratio = 0
    else:
        ratio = btc_value / total_assets

    if ratio >= 0.75:
        score = 5
        rationale = "The majority of treasury assets are held in bitcoin."
    elif ratio >= 0.6:
        score = 4
        rationale = "Bitcoin is the dominant allocation in the treasury."
    elif ratio >= 0.4:
        score = 3
        rationale = "Holdings are balanced between bitcoin and cash."
    elif ratio >= 0.2:
        score = 2
        rationale = "Cash holdings outweigh bitcoin, signalling caution."
    else:
        score = 1
        rationale = "Bitcoin is a minor portion of the treasury."

    if market_price <= profile.internal_price_per_btc * 0.97:
        commentary = (
            "BitMine is likely to accumulate below their internal valuation."
        )
    elif market_price >= profile.internal_price_per_btc * 1.03:
        commentary = (
            "BitMine may trim their position above the benchmark price."
        )
    else:
        commentary = (
            "BitMine appears content to maintain current exposure near fair value."
        )

    return {
        "score": score,
        "ratio": ratio,
        "rationale": rationale,
        "commentary": commentary,
    }

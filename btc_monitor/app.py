from __future__ import annotations

from flask import Flask, jsonify, render_template

from .bitmine import BITMINE_PROFILE, evaluate_arbitrage, evaluate_true_believer
from .market import format_currency, get_btc_price


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def dashboard():
        price, source = get_btc_price()
        arbitrage = evaluate_arbitrage(price, BITMINE_PROFILE)
        believer = evaluate_true_believer(BITMINE_PROFILE, price)
        holdings_value = BITMINE_PROFILE.btc_holdings * price

        return render_template(
            "index.html",
            price=price,
            price_display=format_currency(price),
            price_source=source,
            bitmine=BITMINE_PROFILE,
            holdings_value=format_currency(holdings_value),
            arbitrage=arbitrage,
            believer=believer,
            format_currency=format_currency,
        )

    @app.route("/api/bitmine")
    def bitmine_api():
        price, source = get_btc_price()
        arbitrage = evaluate_arbitrage(price, BITMINE_PROFILE)
        believer = evaluate_true_believer(BITMINE_PROFILE, price)

        return jsonify(
            {
                "price_usd": price,
                "price_source": source,
                "bitmine": {
                    "name": BITMINE_PROFILE.name,
                    "btc_holdings": BITMINE_PROFILE.btc_holdings,
                    "internal_price_per_btc": BITMINE_PROFILE.internal_price_per_btc,
                    "usd_liquidity": BITMINE_PROFILE.usd_liquidity,
                    "strategic_notes": BITMINE_PROFILE.strategic_notes,
                },
                "holdings_value_usd": BITMINE_PROFILE.btc_holdings * price,
                "arbitrage": arbitrage,
                "true_believer": believer,
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

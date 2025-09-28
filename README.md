# BitMine BTC Monitor

A lightweight Flask dashboard that displays the latest Bitcoin (BTC) spot
price alongside BitMine's treasury profile. The page highlights potential
arbitrage opportunities between BitMine's internal benchmark and the live
market, and estimates how much of a "true believer" the company is on a
1–5 scale based on their treasury allocation.

## Features

- Fetches the latest BTC/USD price from the Coindesk public API with a
  graceful offline fallback.
- Shows the market value of BitMine's disclosed holdings.
- Flags arbitrage opportunities when BitMine's benchmark diverges
  materially from the market price.
- Scores BitMine's conviction in bitcoin using a transparent heuristic.
- Provides both a web dashboard and a JSON API at `/api/bitmine`.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Once the server is running, open <http://localhost:8000> in a browser to
view the dashboard.

## Testing

To ensure the application has no syntax errors you can run:

```bash
python -m compileall .
```

The command compiles all Python files and fails if there are syntax
issues.

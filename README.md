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

## Run it locally

These commands clone the repository, install the dependencies, and launch
an HTTP server listening on <http://localhost:8000>.

```bash
# Clone the project from GitHub and move into the directory
git clone https://github.com/<your-account>/btc_monitor.git
cd btc_monitor

# Create an isolated Python environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Start the web dashboard
python -m btc_monitor
```

After the server starts, open <http://localhost:8000> in a browser to view
the dashboard. The JSON representation of the same data lives at
<http://localhost:8000/api/bitmine>.

To stop the server press `Ctrl+C` in the terminal where it is running.

## Alternative entry points

- **Flask CLI:** `flask --app btc_monitor.app run --port 8000 --debug`
- **Gunicorn (production-style):** `gunicorn --bind 0.0.0.0:8000 btc_monitor:app`

## Testing

To ensure the application has no syntax errors you can run:

```bash
python -m compileall .
```

The command compiles all Python files and fails if there are syntax
issues.

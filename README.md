# Gemini Trading Bot

This project is a Python-based automated trading bot that uses the Google Gemini API for market analysis and the Upstox API for trade execution.

## ⚠️ Disclaimer

Automated trading is highly risky and can result in significant financial loss. This project is for educational purposes only. Use it at your own risk. **It is strongly recommended to test thoroughly in a sandbox (paper trading) environment before using real money.**

## Features

- **AI-Powered Analysis:** Uses Google's Gemini Pro model to analyze historical candle data and decide whether to BUY, SELL, or HOLD.
- **Upstox Integration:** Connects to the Upstox API to fetch live market data and execute trades programmatically.
- **Modular Design:** Code is separated into a main application loop, an Upstox client, and the core trading logic.
- **Unit Tested:** The core trading logic is validated with unit tests.

## Setup and Usage

Follow these steps to set up and run the trading bot:

### 1. Clone the Repository

First, get the code on your local machine.

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Install Dependencies

Create a virtual environment and install the required Python packages from the `requirements.txt` file.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure the Bot

You must provide your own API credentials to run the bot. Open the `gemini_trader/main.py` file and edit the `CONFIG` dictionary at the top of the file:

- **`GEMINI_API_KEY`**: Paste your API key from Google AI Studio.
- **`UPSTOX_ACCESS_TOKEN`**: Paste a valid access token for the Upstox API. You need to generate this token through the Upstox OAuth2 login flow. This token is short-lived and will need to be refreshed.

```python
# gemini_trader/main.py

CONFIG = {
    "API_KEYS": {
        "GEMINI_API_KEY": "PASTE_YOUR_GEMINI_API_KEY_HERE"
    },
    # ...
    "UPSTOX_ACCESS_TOKEN": "PASTE_YOUR_UPSTOX_ACCESS_TOKEN_HERE"
}
```

You can also configure the trading parameters like the stock `INSTRUMENT`, `QUANTITY`, and `INTERVAL`.

### 4. Run the Bot

Once configured, you can start the bot by running the `main.py` script:

```bash
python gemini_trader/main.py
```

The bot will start running in a loop, fetching data, analyzing it, and printing its decisions to the console. To stop the bot, press `Ctrl+C`.

## Testing

The project includes unit tests for the trading logic. You can run them using `pytest`:

```bash
PYTHONPATH=. pytest
```

It is highly recommended to first run the bot against the Upstox sandbox environment. To do this, you will need sandbox credentials from Upstox and you will need to modify the `UpstoxClient` initialization in `gemini_trader/main.py` to `upstox_client = UpstoxClient(access_token=upstox_access_token, sandbox=True)`.

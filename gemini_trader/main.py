# Main application file for the Gemini Trader bot.
# This file will contain the main loop that runs the trading bot.

import time
from datetime import datetime, timedelta

from upstox_client import UpstoxClient
from trading_logic import TradingLogic

# --- TEMPORARY WORKAROUND ---
# The configuration is hardcoded here because of a persistent
# issue with creating the config.ini file in this environment.
# Ideally, this should be loaded from an external config file.
CONFIG = {
    "API_KEYS": {
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY"
    },
    "TRADING": {
        "INSTRUMENT": "NSE_EQ|INE848E01016", # Example: Reliance Industries
        "QUANTITY": 1,
        "INTERVAL": "1minute", # See Upstox API docs for options
        "LOOP_INTERVAL_SECONDS": 60
    },
    "UPSTOX_ACCESS_TOKEN": "PASTE_YOUR_UPSTOX_ACCESS_TOKEN_HERE"
}
# --- END OF WORKAROUND ---

def main():
    """
    Main function to run the trading bot.
    """
    print("🚀 Starting Gemini Trader Bot...")

    # --- Configuration ---
    gemini_api_key = CONFIG["API_KEYS"]["GEMINI_API_KEY"]
    upstox_access_token = CONFIG["UPSTOX_ACCESS_TOKEN"]
    instrument = CONFIG["TRADING"]["INSTRUMENT"]
    quantity = CONFIG["TRADING"]["QUANTITY"]
    interval = CONFIG["TRADING"]["INTERVAL"]
    loop_interval = CONFIG["TRADING"]["LOOP_INTERVAL_SECONDS"]

    # --- Critical User Input Check ---
    if "YOUR_GEMINI_API_KEY" in gemini_api_key:
        print("🛑 ERROR: Please replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key.")
        return
    if "PASTE_YOUR_UPSTOX_ACCESS_TOKEN_HERE" in upstox_access_token:
        print("🛑 ERROR: Please replace 'PASTE_YOUR_UPSTOX_ACCESS_TOKEN_HERE' with a valid Upstox access token.")
        print("INFO: You need to generate this token via the Upstox OAuth2 login flow.")
        return

    # --- Initialization ---
    # IMPORTANT: Before running with real money, it is highly recommended to use
    # the Upstox sandbox environment for paper trading. You can do this by
    # modifying the UpstoxClient initialization to include `sandbox=True`.
    # You will need separate sandbox credentials from Upstox.
    try:
        upstox_client = UpstoxClient(access_token=upstox_access_token)
        trading_logic = TradingLogic(gemini_api_key=gemini_api_key)
    except ValueError as e:
        print(f"🛑 ERROR: Failed to initialize clients. {e}")
        return

    print("✅ Clients initialized successfully.")

    # --- Main Trading Loop ---
    while True:
        try:
            print(f"\n----- New Iteration: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----")

            # 1. Get historical data
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d') # Fetch last 5 days for context

            print(f"Fetching historical data for {instrument} from {from_date} to {to_date}...")
            historical_data = upstox_client.get_historical_candle_data(instrument, interval, to_date, from_date)

            if not historical_data or not historical_data.get('data', {}).get('candles'):
                print("⚠️ Warning: Could not fetch historical data. Skipping this iteration.")
                time.sleep(loop_interval)
                continue

            # 2. Get trading decision from Gemini
            print("Analyzing data with Gemini...")
            decision = trading_logic.analyze_market_data(historical_data)

            # 3. Execute trade based on decision
            if decision == "BUY":
                print(f"🔥 Decision: BUY. Placing BUY order for {quantity} unit(s) of {instrument}.")
                # Note: Upstox product codes: D=Delivery, I=Intraday
                order_response = upstox_client.place_order(
                    quantity=quantity,
                    product='I', # Intraday
                    validity='DAY',
                    instrument_token=instrument,
                    order_type='MARKET',
                    transaction_type='BUY'
                )
                print(f"Order response: {order_response}")
            elif decision == "SELL":
                print(f"💰 Decision: SELL. Placing SELL order for {quantity} unit(s) of {instrument}.")
                order_response = upstox_client.place_order(
                    quantity=quantity,
                    product='I', # Intraday
                    validity='DAY',
                    instrument_token=instrument,
                    order_type='MARKET',
                    transaction_type='SELL'
                )
                print(f"Order response: {order_response}")
            else: # HOLD
                print("💤 Decision: HOLD. No action taken.")

            # 4. Wait for the next interval
            print(f"Waiting for {loop_interval} seconds...")
            time.sleep(loop_interval)

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            print("Waiting for a moment before retrying...")
            time.sleep(loop_interval)


if __name__ == "__main__":
    main()

# This module will contain the core trading logic.
# It will use the Upstox client to get data and the Gemini API to make trading decisions.

import google.generativeai as genai
import json

class TradingLogic:
    def __init__(self, gemini_api_key):
        """
        Initializes the Trading Logic module.
        """
        if not gemini_api_key or gemini_api_key == "YOUR_GEMINI_API_KEY":
            raise ValueError("A valid Gemini API key is required.")

        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print("Trading Logic initialized with Gemini model.")

    def analyze_market_data(self, historical_data):
        """
        Analyzes historical market data using the Gemini API to get a trading decision.

        :param historical_data: A list of candle data from the Upstox API.
        :return: A string "BUY", "SELL", or "HOLD".
        """
        if not historical_data:
            print("No historical data provided to analyze.")
            return "HOLD"

        # Convert the candle data to a more readable format for the prompt
        formatted_data = self._format_data_for_prompt(historical_data)

        prompt = self._create_prompt(formatted_data)

        try:
            print("Sending request to Gemini API...")
            response = self.model.generate_content(prompt)
            decision = self._parse_gemini_response(response.text)
            print(f"Gemini's decision: {decision}")
            return decision
        except Exception as e:
            print(f"An error occurred while calling the Gemini API: {e}")
            return "HOLD" # Default to HOLD on error

    def _format_data_for_prompt(self, historical_data):
        """
        Formats the candle data into a simple string.
        """
        # Let's just use the last 10 candles for the prompt to keep it concise
        recent_data = historical_data['data']['candles'][-10:]

        formatted_string = "Timestamp, Open, High, Low, Close, Volume\n"
        for candle in recent_data:
            formatted_string += f"{candle[0]}, {candle[1]}, {candle[2]}, {candle[3]}, {candle[4]}, {candle[5]}\n"
        return formatted_string

    def _create_prompt(self, formatted_data):
        """
        Creates the prompt to be sent to the Gemini API.
        """
        prompt = f"""
        You are an expert intraday stock market analyst. Your task is to analyze the provided market data and recommend a trading action.
        Your response must be a single word: BUY, SELL, or HOLD. Do not provide any explanation or other text.

        Here is the recent candle data for a stock (Timestamp, Open, High, Low, Close, Volume):
        {formatted_data}

        Based on this data, what is your trading recommendation?
        """
        return prompt

    def _parse_gemini_response(self, response_text):
        """
        Parses the response from Gemini to extract the trading decision.
        """
        # The response should be a single word. We'll look for BUY, SELL, or HOLD in the text.
        response_upper = response_text.upper()
        if "BUY" in response_upper:
            return "BUY"
        elif "SELL" in response_upper:
            return "SELL"
        else:
            return "HOLD"

if __name__ == '__main__':
    # This is for testing purposes.
    # You would need a valid Gemini API key to run this.
    # We are mocking the data that would come from the Upstox API.

    # Mock historical data from Upstox
    mock_historical_data = {
        'data': {
            'candles': [
                ['2023-10-20T14:00:00+05:30', 100, 102, 99, 101, 1000],
                ['2023-10-20T14:01:00+05:30', 101, 103, 100, 102, 1200],
                ['2023-10-20T14:02:00+05:30', 102, 104, 101, 103, 1500],
                ['2023-10-20T14:03:00+05:30', 103, 103, 102, 102.5, 1300],
                ['2023-10-20T14:04:00+05:30', 102.5, 103.5, 102, 103, 1100],
            ]
        }
    }

    try:
        # NOTE: This will fail unless you set a valid Gemini API key in your environment
        # or replace "YOUR_GEMINI_API_KEY" with a real key.
        # For this test, we expect a ValueError.
        logic = TradingLogic(gemini_api_key="YOUR_GEMINI_API_KEY")
        # decision = logic.analyze_market_data(mock_historical_data)
        # print(f"Test decision: {decision}")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("Trading logic script finished execution.")

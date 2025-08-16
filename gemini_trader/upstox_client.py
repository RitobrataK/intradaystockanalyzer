# This module will contain the Upstox API client.
# It will handle authentication, placing orders, and fetching market data.

import upstox_client
from upstox_client.rest import ApiException
import os

class UpstoxClient:
    def __init__(self, access_token=None, sandbox=False):
        """
        Initializes the Upstox client.
        :param access_token: The OAuth2 access token for authentication.
        :param sandbox: If True, connects to the sandbox environment.
        """
        if not access_token:
            raise ValueError("An access_token is required to initialize the UpstoxClient.")

        # Configure OAuth2 access token for authorization: OAUTH2
        configuration = upstox_client.Configuration()

        if sandbox:
            # Use the sandbox host
            configuration.host = "https://api-sandbox.upstox.com/v2"
            print("INFO: Upstox client is running in SANDBOX mode.")

        configuration.access_token = access_token

        self.api_client = upstox_client.ApiClient(configuration)
        self.history_api = upstox_client.HistoryApi(self.api_client)
        self.order_api = upstox_client.OrderApi(self.api_client)

        print("Upstox Client initialized successfully.")

    def get_historical_candle_data(self, instrument_key, interval, to_date, from_date):
        """
        Fetches historical candle data.
        :param instrument_key: e.g., 'NSE_EQ|INE848E01016'
        :param interval: e.g., '1minute', 'day'
        :param to_date: 'YYYY-MM-DD'
        :param from_date: 'YYYY-MM-DD'
        :return: API response or None on error
        """
        try:
            # Historical candle data
            api_version = 'v2'
            api_response = self.history_api.get_historical_candle_data3(instrument_key, interval, to_date, from_date, api_version)
            return api_response
        except ApiException as e:
            print(f"Exception when calling HistoryApi->get_historical_candle_data: {e}\n")
            return None

    def place_order(self, quantity, product, validity, instrument_token, order_type, transaction_type, price=0.0, trigger_price=0.0, disclosed_quantity=0, is_amo=False):
        """
        Places an order.
        """
        try:
            api_version = 'v2'
            order_data = upstox_client.PlaceOrderRequest(
                quantity=quantity,
                product=product,
                validity=validity,
                instrument_token=instrument_token,
                order_type=order_type,
                transaction_type=transaction_type,
                price=price,
                trigger_price=trigger_price,
                disclosed_quantity=disclosed_quantity,
                is_amo=is_amo
            )
            api_response = self.order_api.place_order(order_data, api_version)
            return api_response
        except ApiException as e:
            print(f"Exception when calling OrderApi->place_order: {e}\n")
            return None

if __name__ == '__main__':
    # This is for testing purposes.
    # You would need a valid access token to run this.
    # The access token can be obtained via the Upstox OAuth2 flow.
    # For now, we are just checking if the class structure is okay.

    # This will fail without a real token, which is expected.
    try:
        client = UpstoxClient(access_token="DUMMY_ACCESS_TOKEN")
        # Example usage (will not work with a dummy token)
        # candles = client.get_historical_candle_data('NSE_EQ|INE848E01016', '1minute', '2023-10-20', '2023-10-19')
        # if candles:
        #     print(candles)
    except ValueError as e:
        print(e)

    print("Upstox client script finished execution.")

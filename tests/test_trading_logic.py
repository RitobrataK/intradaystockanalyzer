import pytest
from gemini_trader.trading_logic import TradingLogic

@pytest.fixture
def mock_gemini_model(mocker):
    """Fixture to mock the Gemini generative model."""
    mock_model = mocker.patch('google.generativeai.GenerativeModel', autospec=True)
    # The 'generate_content' method is on the instance, so we mock it on the return value of the constructor
    mocker.patch('google.generativeai.configure')
    mocker.patch.object(mock_model.return_value, 'generate_content')
    return mock_model.return_value

# Mock historical data from Upstox
MOCK_HISTORICAL_DATA = {
    'data': {
        'candles': [
            ['2023-10-20T14:00:00+05:30', 100, 102, 99, 101, 1000],
            ['2023-10-20T14:01:00+05:30', 101, 103, 100, 102, 1200],
            ['2023-10-20T14:02:00+05:30', 102, 104, 101, 103, 1500],
        ]
    }
}

def test_trading_logic_initialization():
    """Test that TradingLogic initializes correctly."""
    logic = TradingLogic(gemini_api_key="fake_key")
    assert logic.model is not None

def test_decision_is_buy(mock_gemini_model):
    """Test that the logic correctly identifies a BUY signal."""
    # Configure the mock to return a response object with a 'text' attribute
    mock_gemini_model.generate_content.return_value.text = "BUY"

    logic = TradingLogic(gemini_api_key="fake_key")
    decision = logic.analyze_market_data(MOCK_HISTORICAL_DATA)
    assert decision == "BUY"

def test_decision_is_sell(mock_gemini_model):
    """Test that the logic correctly identifies a SELL signal."""
    mock_gemini_model.generate_content.return_value.text = "The analysis suggests a strong SELL signal."

    logic = TradingLogic(gemini_api_key="fake_key")
    decision = logic.analyze_market_data(MOCK_HISTORICAL_DATA)
    assert decision == "SELL"

def test_decision_is_hold_on_ambiguous_response(mock_gemini_model):
    """Test that the logic defaults to HOLD on an ambiguous response."""
    mock_gemini_model.generate_content.return_value.text = "The market is uncertain. It might be good to wait."

    logic = TradingLogic(gemini_api_key="fake_key")
    decision = logic.analyze_market_data(MOCK_HISTORICAL_DATA)
    assert decision == "HOLD"

def test_decision_is_hold_on_empty_data():
    """Test that the logic returns HOLD if no historical data is provided."""
    logic = TradingLogic(gemini_api_key="fake_key")
    decision = logic.analyze_market_data(None)
    assert decision == "HOLD"

def test_prompt_creation(mocker):
    """Test that the prompt is created with the correct structure."""
    logic = TradingLogic(gemini_api_key="fake_key")

    # Spy on the final method that receives the prompt
    generate_content_spy = mocker.spy(logic.model, 'generate_content')

    # Mock the response parser to avoid errors after the spy
    mocker.patch.object(logic, '_parse_gemini_response', return_value="HOLD")

    logic.analyze_market_data(MOCK_HISTORICAL_DATA)

    # Check that generate_content was called and inspect the prompt it received
    generate_content_spy.assert_called_once()
    final_prompt = generate_content_spy.call_args[0][0] # Get the first argument

    assert "You are an expert intraday stock market analyst." in final_prompt
    assert "Timestamp, Open, High, Low, Close, Volume" in final_prompt
    assert "100, 102, 99, 101, 1000" in final_prompt # Check for data from our mock

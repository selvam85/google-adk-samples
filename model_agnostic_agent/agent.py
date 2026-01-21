"""
Model-Agnostic Agent Example
Change the LITELLM_MODEL environment variable to switch providers.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.apps.app import App
from google.adk.models.lite_llm import LiteLlm

load_dotenv()


# Configuration - change this to switch models
DEFAULT_MODEL = "gemini/gemini-3-flash-preview"


def get_model():
    """Get the model from environment or use default."""
    model_string = os.getenv("LITELLM_MODEL", DEFAULT_MODEL)
    print(f"Using model: {model_string}")
    return LiteLlm(model=model_string)


# Hardcoded data for tools
WEATHER_DATA = {
    "new york": {"city": "New York", "temperature": "45°F", "condition": "Cloudy"},
    "los angeles": {"city": "Los Angeles", "temperature": "72°F", "condition": "Sunny"},
    "chicago": {"city": "Chicago", "temperature": "28°F", "condition": "Snowy"},
    "miami": {"city": "Miami", "temperature": "82°F", "condition": "Partly Cloudy"}
}

STOCK_DATA = {
    "AAPL": {"ticker": "AAPL", "company": "Apple Inc.", "price": "$185.50"},
    "GOOGL": {"ticker": "GOOGL", "company": "Alphabet Inc.", "price": "$142.25"},
    "MSFT": {"ticker": "MSFT", "company": "Microsoft Corp.", "price": "$378.90"},
    "AMZN": {"ticker": "AMZN", "company": "Amazon.com Inc.", "price": "$178.35"}
}


# Tools
def get_weather(city: str) -> dict:
    """Get the current weather for a city.

    Args:
        city: The name of the city

    Returns:
        Weather information for the city
    """
    city_lower = city.lower().strip()
    if city_lower in WEATHER_DATA:
        return WEATHER_DATA[city_lower]
    return {
        "status": "unsupported",
        "message": f"Weather data not available for '{city}'. Supported cities: New York, Los Angeles, Chicago, Miami"
    }


def get_stock_price(ticker: str) -> dict:
    """Get the current stock price for a ticker symbol.

    Args:
        ticker: The stock ticker symbol (e.g., AAPL, GOOGL)

    Returns:
        Stock price information
    """
    ticker_upper = ticker.upper().strip()
    if ticker_upper in STOCK_DATA:
        return STOCK_DATA[ticker_upper]
    return {
        "status": "unsupported",
        "message": f"Stock price not available for '{ticker}'. Supported tickers: AAPL, GOOGL, MSFT, AMZN"
    }


# Create agent with configurable model
assistant = LlmAgent(
    name="assistant",
    model=get_model(), # Get the model from the environment variable instead of hardcoding it
    instruction="""You are a helpful assistant that can:
    - Answer questions using your knowledge
    - Get weather information for any city using get_weather tool
    - Get stock prices for any ticker symbol using get_stock_price tool

    Be concise and helpful in your responses.
    """,
    tools=[get_weather, get_stock_price]
)


app = App(
    name="model_agnostic_agent",
    root_agent=assistant
)

"""
Travel Assistant Agent
An agent that helps users plan travel with flights, hotels, currency, and web search.
"""

from dotenv import load_dotenv
from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# ============ Sample Data ============

FLIGHTS = {
    "AA123": {"airline": "American Airlines", "origin": "JFK", "destination": "LAX", "departure": "2026-03-15 08:00", "arrival": "2026-03-15 11:30", "status": "On Time", "gate": "B22"},
    "UA456": {"airline": "United Airlines", "origin": "SFO", "destination": "ORD", "departure": "2026-03-15 14:00", "arrival": "2026-03-15 20:15", "status": "Delayed", "delay_minutes": 45, "gate": "C17"},
    "DL789": {"airline": "Delta Airlines", "origin": "ATL", "destination": "MIA", "departure": "2026-03-15 10:30", "arrival": "2026-03-15 12:45", "status": "Boarding", "gate": "A5"},
}

HOTELS = {
    "paris": [
        {"id": "H001", "name": "Hotel Le Marais", "stars": 4, "price_per_night": 180, "available": True, "amenities": ["WiFi", "Breakfast", "Pool"]},
        {"id": "H002", "name": "Boutique Saint-Germain", "stars": 5, "price_per_night": 320, "available": True, "amenities": ["WiFi", "Spa", "Restaurant", "Gym"]},
        {"id": "H003", "name": "Paris Budget Inn", "stars": 2, "price_per_night": 75, "available": True, "amenities": ["WiFi"]},
    ],
    "tokyo": [
        {"id": "H004", "name": "Shinjuku Grand Hotel", "stars": 4, "price_per_night": 150, "available": True, "amenities": ["WiFi", "Restaurant", "Onsen"]},
        {"id": "H005", "name": "Shibuya Capsule Hotel", "stars": 2, "price_per_night": 45, "available": True, "amenities": ["WiFi", "Locker"]},
        {"id": "H006", "name": "Imperial Tokyo", "stars": 5, "price_per_night": 450, "available": False, "amenities": ["WiFi", "Spa", "Pool", "Restaurant", "Gym"]},
    ],
    "london": [
        {"id": "H007", "name": "The Westminster", "stars": 4, "price_per_night": 200, "available": True, "amenities": ["WiFi", "Breakfast", "Bar"]},
        {"id": "H008", "name": "Covent Garden Suites", "stars": 5, "price_per_night": 380, "available": True, "amenities": ["WiFi", "Spa", "Restaurant", "Theater tickets"]},
    ],
}


# ============ Custom Function Tools ============

def get_flight_status(flight_number: str) -> dict:
    """Get the current status of a flight.

    Use this tool when a user asks about their flight status, departure time,
    arrival time, gate information, or delays.

    Args:
        flight_number: The flight number (e.g., "AA123", "UA456")

    Returns:
        Flight details including status, times, and gate information
    """
    flight_number = flight_number.upper().strip()

    if flight_number not in FLIGHTS:
        return {
            "found": False,
            "error": f"Flight '{flight_number}' not found.",
            "hint": "Try: AA123, UA456, or DL789"
        }

    flight = FLIGHTS[flight_number]
    result = {
        "found": True,
        "flight_number": flight_number,
        "airline": flight["airline"],
        "route": f"{flight['origin']} → {flight['destination']}",
        "departure": flight["departure"],
        "arrival": flight["arrival"],
        "status": flight["status"],
        "gate": flight["gate"]
    }

    if "delay_minutes" in flight:
        result["delay"] = f"{flight['delay_minutes']} minutes"

    return result


def search_hotels(city: str, check_in: str, check_out: str, guests: int = 2) -> dict:
    """Search for available hotels in a city.

    Use this tool when a user wants to find hotels, accommodation, or places to stay.

    Args:
        city: Destination city (e.g., "Paris", "Tokyo", "London")
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        guests: Number of guests (default: 2)

    Returns:
        List of available hotels with prices and amenities
    """
    city_lower = city.lower().strip()

    if city_lower not in HOTELS:
        return {
            "found": 0,
            "error": f"No hotels in '{city}'. Available: Paris, Tokyo, London"
        }

    available = [h for h in HOTELS[city_lower] if h["available"]]

    if not available:
        return {"found": 0, "message": f"No availability in {city} for those dates."}

    try:
        d1 = datetime.strptime(check_in, "%Y-%m-%d")
        d2 = datetime.strptime(check_out, "%Y-%m-%d")
        nights = max((d2 - d1).days, 1)
    except ValueError:
        nights = 1

    results = []
    for hotel in available:
        results.append({
            "id": hotel["id"],
            "name": hotel["name"],
            "stars": "⭐" * hotel["stars"],
            "price_per_night": f"${hotel['price_per_night']}",
            "total": f"${hotel['price_per_night'] * nights}",
            "amenities": hotel["amenities"]
        })

    return {"found": len(results), "city": city, "nights": nights, "hotels": results}


# ============ Search Agent (Built-in Tool) ============

search_agent = Agent(
    name='web_search',
    model='gemini-3-flash-preview',
    description='Search the web for real-time travel information',
    instruction="""You are a travel research specialist. Search for:
    - Weather conditions and forecasts
    - Local events and festivals
    - Travel advisories and visa requirements
    - Popular attractions and restaurants

    Provide concise, helpful information.""",
    tools=[google_search],
)


# ============ Main Travel Assistant (Agent as Tool + Custom Tools) ============

root_agent = Agent(
    name="travel_assistant",
    model="gemini-3-flash-preview",
    instruction="""You are a helpful travel assistant that helps users plan trips.

You can help with:
1. **Flight Status** - Check if flights are on time, delayed, or boarding
2. **Hotel Search** - Find available hotels in Paris, Tokyo, or London
3. **Travel Research** - Search the web for weather, events, attractions, and travel tips

Guidelines:
- Always use tools to look up information - don't make up data
- For flight status, ask for the flight number if not provided
- When showing hotels, highlight price, rating, and key amenities
- Use web search for current weather, events, or destination tips

Sample flight numbers for testing: AA123, UA456, DL789
Sample cities with hotels: Paris, Tokyo, London""",
    tools=[
        get_flight_status,
        search_hotels,
        AgentTool(agent=search_agent),  # Agent as a tool!
    ]
)


async def main():
    """Run the travel assistant with ADK Runner."""

    # Load environment variables from .env file for Google API key
    load_dotenv()

    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name="travel_assistant",
        session_service=session_service,
    )

    print("Travel Assistant Ready!")
    print("Try these prompts:")
    print("- What's the status of flight AA123?")
    print("- Find hotels in Paris for March 15-20, 2026")
    print("- What's the weather like in Tokyo?")

    user_id = "demo_user"
    session_id = "demo_session"

    # Create session before running - run_async requires existing session
    await session_service.create_session(
        app_name="travel_assistant",
        user_id=user_id,
        session_id=session_id
    )

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ['quit', 'exit', 'q']:
            break

        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=user_input)]
        )

        print("\nAssistant: ", end="", flush=True)

        try:
            async for event in runner.run_async(
                session_id=session_id,
                user_id=user_id,
                new_message=content
            ):
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                print(part.text, end="", flush=True)
        except Exception as e:
            print("Error in run_async", {"error": str(e)})
            raise e
        print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
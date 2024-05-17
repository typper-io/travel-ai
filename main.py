import os
import requests
import json
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

def search_google_flights(departure_id, arrival_id, departure_date, return_date, currency="USD"):
    """Use this function to find flights on Google.

    Args:
        departure_id (str): The departure airport code.
        arrival_id (str): The arrival airport code.
        departure_date (str): The departure date in the format "YYYY-MM-DD".
        return_date (str): The return date in the format "YYYY-MM-DD".
        currency (str): The currency code (default is "USD").

    Returns:
        str: A JSON string of flights.
    """
    
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": departure_date,
        "return_date": return_date,
        "currency": currency,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} with response: {response.text}")
        return f"Received status code {response.status_code} with response: {response.text}"
    
    results = response.json()
    
    if 'error' in results:
        print(f"Error in response: {results['error']}")
        return []
    
    best_flights = results.get('best_flights', [])
    other_flights = results.get('other_flights', [])

    flights = best_flights + other_flights

    simplified_flights = []

    for flight_group in flights:
        
        for flight in flight_group["flights"]:
            simplified_flight = {
                "departure_airport": flight.get("departure_airport", {}).get("name"),
                "departure_time": flight.get("departure_airport", {}).get("time"),
                "arrival_airport": flight.get("arrival_airport", {}).get("name"),
                "arrival_time": flight.get("arrival_airport", {}).get("time"),
                "duration": flight.get("duration"),
                "airplane": flight.get("airplane"),
                "airline": flight.get("airline"),
                "flight_number": flight.get("flight_number"),
                "travel_class": flight.get("travel_class")
            }

            simplified_flights.append(simplified_flight)
                
    if not simplified_flights:
        print("No flights found.")
    
    return json.dumps(simplified_flights)

def search_google_hotels(destination, type, check_in_date, check_out_date, adults=1, currency="USD"):
    """Use this function to find hotels on Google.

    Args:
        destination (str): The destination city or region.
        type (str): The type of accommodation (e.g., "Resorts", "Hotels").
        check_in_date (str): The check-in date in the format "YYYY-MM-DD".
        check_out_date (str): The check-out date in the format "YYYY-MM-DD".
        adults (int): The number of adults (default is 1).
        currency (str): The currency code (default is "USD").

    Returns:
        str: A JSON string of hotels.
    """

    params = {
        "engine": "google_hotels",
        "q": destination + type,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} with response: {response.text}")
        return f"Received status code {response.status_code} with response: {response.text}"
    
    results = response.json()
    
    if 'error' in results:
        print(f"Error in response: {results['error']}")
        return []
    
    hotels = results.get('properties', [])

    simplified_hotels = []

    for property in hotels:
        simplified_property = {
            "name": property.get("name"),
            "latitude": property.get("gps_coordinates", {}).get("latitude"),
            "longitude": property.get("gps_coordinates", {}).get("longitude"),
            "check_in_time": property.get("check_in_time"),
            "check_out_time": property.get("check_out_time"),
            "rate_per_night": property.get("rate_per_night", {}).get("lowest", None),
            "total_rate": property.get("total_rate", {}).get("lowest", None),
            "overall_rating": property.get("overall_rating"),
            "reviews": property.get("reviews"),
            "location_rating": property.get("location_rating"),
            "amenities": property.get("amenities")
        }

        simplified_hotels.append(simplified_property)
    
    if not simplified_hotels:
        print("No flights found.")
    
    return json.dumps(simplified_hotels)

assistant = Assistant(
    llm=OpenAIChat(model="gpt-4o"),
    description="You are a travel planner AI that helps users organize their perfect trips.",
    instructions=[
        "Start by asking the user for their travel preferences and details such as origin, destination, departure date, return date, check-in and check-out dates.",
        "Use the search_google_flights function to find flights matching the user's criteria.",
        "Use the search_google_hotels function to find hotels matching the user's criteria.",
        "Summarize the top two flight and hotel options, including links, dates, and prices.",
        "Use DuckDuckGo to find popular activities and attractions in the user's destination.",
        "Create a suggested itinerary including flights, hotels, and activities, with estimated costs and trip duration.",
        "Read and consult the chat history to avoid missing any user information.",
        "Return the total estimated cost of the trip and the duration of the trip.",
    ],
    debug_mode=False,
    tools=[DuckDuckGo(), search_google_flights, search_google_hotels], 
    show_tool_calls=True, 
    read_chat_history=True,
    add_datetime_to_instructions=True,
)
assistant.cli_app(markdown=True)

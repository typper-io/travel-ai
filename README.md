<div style="text-align: center;">
    <img src="assets/logo.png" alt="Logo" width="100">
</div>

# Travel AI

Typper's POC: Plan and discover perfect trips with Phidata and OpenAI using smart prompts.

## Description

This project is a Proof of Concept (POC) by Typper, utilizing Phidata and OpenAI to plan and search for trips based on user prompts. The AI assistant helps users organize their perfect trips by finding the best flights, hotels, and popular activities in their desired destination.

## Features

- **Flight Search**: Uses Google Flights to find the best flights matching the user's criteria.
- **Hotel Search**: Uses Google Hotels to find the best accommodations based on the user's preferences.
- **Activity Suggestions**: Recommends popular activities and attractions at the destination.
- **Itinerary Creation**: Compiles a suggested itinerary with estimated costs and trip duration.

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/travel-ai.git
    cd travel-ai
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your SerpAPI and OpenAI API keys:

    ```
    SERPAPI_API_KEY=your_serpapi_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

To run the assistant, simply execute the script:

```sh
python main.py
```

## Functions

**search_google_flights**

Finds flights on Google Flights.

**Args**:

- departure_id (str): The departure airport code.
- arrival_id (str): The arrival airport code.
- departure_date (str): The departure date in the format "YYYY-MM-DD".
- return_date (str): The return date in the format "YYYY-MM-DD".
- currency (str): The currency code (default is "USD").

**Returns**:

- str: A JSON string of flights.

**search_google_hotels**

Finds hotels on Google Hotels.

**Args**:

- destination (str): The destination city or region.
- type (str): The type of accommodation (e.g., "Resorts", "Hotels").
- check_in_date (str): The check-in date in the format "YYYY-MM-DD".
- check_out_date (str): The check-out date in the format "YYYY-MM-DD".
- adults (int): The number of adults (default is 1).
- currency (str): The currency code (default is "USD").

**Returns**:

- str: A JSON string of hotels.

## Assistant

The assistant is configured with the following instructions:

1. Ask the user for their travel preferences and details such as origin, destination, departure date, return date, check-in and check-out dates.
2. Use the search_google_flights function to find flights matching the user's criteria.
3. Use the search_google_hotels function to find hotels matching the user's criteria.
4. Summarize the top two flight and hotel options, including links, dates, and prices.
5. Use DuckDuckGo to find popular activities and attractions in the user's destination.
6. Create a suggested itinerary including flights, hotels, and activities, with estimated costs and trip duration.
7. Read and consult the chat history to avoid missing any user information.
8. Return the total estimated cost of the trip and the duration of the trip.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
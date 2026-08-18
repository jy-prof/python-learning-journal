import os
import requests
from dotenv import load_dotenv

load_dotenv()


class FlightSearch:

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

    def search_flights(self, outbound_date, return_date, max_price):
        params = {
            "engine": "google_flights",
            "api_key": self.api_key,
            "departure_id": "LHR,LGW,STN,LTN,LCY",
            "arrival_id": "HND,NRT",
            "outbound_date": outbound_date,
            "return_date": return_date,
            "type": "1",
            "travel_class": "1",
            "adults": "1",
            "currency": "GBP",
            "gl": "uk",
            "hl": "en",
            "sort_by": "2",
            "stops": "2",
            "max_price": max_price,
        }

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=60,
        )

        response.raise_for_status()
        return response.json()

    def find_cheapest(self, data):
        flights = data.get("best_flights", []) + data.get("other_flights", [])

        if not flights:
            return None

        return min(flights, key=lambda flight: flight["price"])

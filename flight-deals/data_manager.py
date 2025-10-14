# This class is responsible for talking to the Google Sheet.
# talks to Sheety to GET/PUT your Google Sheet rows (“prices” sheet)

# 1. Goal: prove you can GET and PUT your sheet via Sheety before touching Amadeus.

import os
import requests
from dotenv import load_dotenv; load_dotenv()
from requests.auth import HTTPBasicAuth
from pprint import pprint


SHEETY_ENDPOINT = "https://api.sheety.co/e0f7b30a1b67463470059db70040bf0f/jyFlightDeals/prices"

class DataManager:

    def __init__(self):
        self.user = os.getenv("SHEETY_USERNAME")
        if not self.user:
            raise ValueError("SHEETY_USERNAME environment variable is not set!")
        self.password = os.getenv("SHEETY_PASSWORD")
        if not self.password:
            raise ValueError("SHEETY_PASSWORD environment variable is not set!")
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.destination_data = []
        # self.max_price = []

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_ENDPOINT, auth=self.authorization)
        data = response.json()
        self.destination_data = data['prices']
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.
        print("Fetched data from Google Sheet successfully.")
        return self.destination_data

    # def get_max_price(self):


    # In the DataManager Class make a PUT request
    # and use the row id from sheet_data to update the Google Sheet with the IATA codes.
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self.authorization
            )
            print(response.text)

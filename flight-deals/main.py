# Glue logic (of main.py):
# 1. Read sheet
# 2. Ensure IATA codes
# 3. Search flights
# 4. Compare prices
# 5. Notify when cheaper


import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
# from pip._internal.cli.cmdoptions import python
# import twilio

# ==================== Set up the Flight Search ==================== #


dm = DataManager()
sheet_data = dm.get_destination_data()
fs = FlightSearch()
nm = NotificationManager()


# set your original airport (origin_city_code)
ORIGIN_CITY_IATA = "LON"


# ==================== Update the Airport Codes in Google Sheet ==================== #

#  check if sheet_data contains any values for the "iataCode" key.
#  If not, update the empty IATA Codes in the Google Sheet.

for city in sheet_data:
    if city['iataCode'] == "":
        city['iataCode'] = fs.get_destination_code(city['city'])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

dm.destination_data = sheet_data
dm.update_destination_codes()

# ==================== Search for Flights ==================== #
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    flights = fs.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination['iataCode'],
        # from_time=tomorrow,
        # to_time=six_month_from_today,
        max_price = destination['lowestPrice']
    )
    cheapest_flight = FlightData.find_cheapest_flight(flights)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        nm.send_whatsapp(  
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly from {cheapest_flight.origin_airport} "
                         f"to {cheapest_flight.destination_airport}, on {cheapest_flight.out_date} until "
                         f"{cheapest_flight.return_date}"
        )

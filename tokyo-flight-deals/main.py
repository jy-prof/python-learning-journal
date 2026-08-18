from datetime import date, timedelta
import time

from flight_search import FlightSearch
from notification_manager import NotificationManager


GOOD_DEAL_PRICE = 550

flight_search = FlightSearch()
notification = NotificationManager()

today = date.today()

trip_lengths = [10, 14]

for days_ahead in range(30, 181, 21):
    outbound_date = today + timedelta(days=days_ahead)

    for trip_length in trip_lengths:
        return_date = outbound_date + timedelta(days=trip_length)

        print(f"Checking {outbound_date} - {return_date}")

        try:
            data = flight_search.search_flights(
                outbound_date.isoformat(),
                return_date.isoformat(),
                GOOD_DEAL_PRICE,
            )

            flight = flight_search.find_cheapest(data)

            if flight:
                price = flight["price"]
                flights = flight["flights"]

                origin = flights[0]["departure_airport"]["id"]
                destination = flights[-1]["arrival_airport"]["id"]

                print(f"Found £{price}: {origin} → {destination}")

                notification.send_message(
                    f"✈️ Tokyo flight deal!\n\n"
                    f"£{price} return\n"
                    f"{outbound_date} → {return_date}\n"
                    f"{origin} → {destination}"
                )

            else:
                print("No deal found.")

        except Exception as error:
            print(f"Error: {error}")

        time.sleep(1)

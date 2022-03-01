import requests as rq
import datetime as dt
import os

TEQUILA_URL = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_KEY = os.environ["TEQUILA_API_KEY"]
FROM_AIRPORT = "AGP"
MONTHS_LIMIT = 8
ROUND_TRIP_TIME = (5, 28)


def reformat_date(date):
    date = dt.datetime.strptime(date[:-8], "%Y-%m-%dT%H:%M")
    date = date.strftime("%d/%m/%Y %H:%M")
    return date


class FlightSearch:
    def __init__(self, criteria_data):
        self.criteria_data = criteria_data
        self.possible_trips: list = []
        self.possible_cities: list = []
        self.found_flights: bool = False

    def fetch_flights(self):
        headers = {
            "apikey": TEQUILA_KEY,
        }

        tomorrow = dt.datetime.now() + dt.timedelta(days=1)
        max_leave_date = tomorrow + dt.timedelta(days=MONTHS_LIMIT * 30)
        min_return_date = tomorrow + dt.timedelta(days=ROUND_TRIP_TIME[0])
        max_return_date = max_leave_date + dt.timedelta(days=ROUND_TRIP_TIME[1])

        tomorrow = tomorrow.strftime("%d/%m/%Y")
        max_leave_date = max_leave_date.strftime("%d/%m/%Y")
        min_return_date = min_return_date.strftime("%d/%m/%Y")
        max_return_date = max_return_date.strftime("%d/%m/%Y")

        for city in self.criteria_data:
            params = {
                "fly_from": FROM_AIRPORT,
                "fly_to": city['iataCode'],
                "date_from": tomorrow,
                "date_to": max_leave_date,
                "return_from": min_return_date,
                "return_to": max_return_date,
                "nights_in_dst_from": f"{ROUND_TRIP_TIME[0]}",
                "nights_in_dst_to": f"{ROUND_TRIP_TIME[1]}",
                "flight_type": "round",
                "adults": "1",
                "selected_cabins": "M",
                "curr": "EUR",
                "locale": "en",
                "price_from": "0",
                "price_to": f"{city['lowestPrice']}",
                "max-stopovers": "0",
                "sort": "price",
                "limit": "10",
            }

            print(f"Requesting flights for {city['city']}...")
            flights_request = rq.get(url=TEQUILA_URL, params=params, headers=headers)
            flights_request.raise_for_status()
            print(f"Found {flights_request.json()['_results']} results for {city['city']}.")
            if flights_request.json()["_results"] > 0:
                self.found_flights = True
                city_count = 0
                self.possible_cities.append(city['city'])
                for trip in flights_request.json()["data"]:
                    if city_count < 15:

                        trip = {
                            "departure": trip["cityTo"],
                            "destination": trip["cityTo"],
                            "price": trip["price"],
                            "departure_date": reformat_date(trip["route"][0]["local_departure"]),
                            "return_date": reformat_date(trip["route"][1]["local_departure"]),
                            "arrival_date": reformat_date(trip["route"][1]["local_arrival"]),
                            "leave_flight": f'{trip["route"][0]["airline"]}{trip["route"][0]["flight_no"]}',
                            "return_flight": f'{trip["route"][1]["airline"]}{trip["route"][1]["flight_no"]}',
                            "leave_departure_airport": trip["route"][0]["flyFrom"],
                            "leave_arrival_airport": trip["route"][0]["flyTo"],
                            "return_departure_airport": trip["route"][1]["flyFrom"],
                            "return_arrival_airport": trip["route"][1]["flyTo"],
                        }
                        self.possible_trips.append(trip)

        print("Compiled possible trips.")

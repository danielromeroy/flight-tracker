import requests as rq
import os

TEQUILA_URL = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_KEY = os.environ["TEQUILA_API_KEY"]


def get_iata(city: str):
    params = {
        "term": city,
        "locale": "en-US",
        "limit": "1",
        "active_only": "true"
    }

    headers = {
        "apikey": TEQUILA_KEY,
    }

    tequila_query = rq.get(url=TEQUILA_URL, params=params, headers=headers)
    tequila_query.raise_for_status()
    return tequila_query.json()["locations"][0]["code"]


class FlightData:
    def __init__(self, criteria_data):
        self.criteria_data = criteria_data
        self.fill_data()

    def fill_data(self):
        for sheet_row in self.criteria_data:
            if sheet_row["iataCode"] == "":
                print(f"Fetching IATA code for {sheet_row['city']}...")
                sheet_row["iataCode"] = get_iata(sheet_row["city"])

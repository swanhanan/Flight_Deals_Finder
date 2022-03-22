import requests
import datetime
from flight_data import FlightData

SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
TEQUILA_API_KEY = os.environ.get('TEQUILA_API_Key')


class FlightSearch:

    def __init__(self):
        self.city_codes = []
    #This class is responsible for talking to the Flight Search API.

    def get_destination_code(self, city_names):
        HEADERS = {"apikey": TEQUILA_API_KEY}
        for city in city_names:
            PARAMS = {"term": city, "location_types": "city" }
            response = requests.get(url=TEQUILA_ENDPOINT, params=PARAMS, headers=HEADERS)
            locations = response.json()["locations"]
            return locations[0]['code']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        HEADERS = {"apikey": TEQUILA_API_KEY}
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.date(),
            "date_to": to_time.date(),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "flight_type": "round",
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=SEARCH_ENDPOINT, params=params, headers=HEADERS)
        try:
            data = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=HEADERS,
                params=params,
            )
            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: ${flight_data.price}")
            return flight_data

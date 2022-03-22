import requests
from pprint import pprint
TOKEN = "SWANFLY"
HEADERS = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
ENDPOINT = "https://api.sheety.co/13eea4da04d7a3ea3019f72c28082354/flightDeals/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}



    def get_destination_data(self):
        response = requests.get(url=ENDPOINT, headers=HEADERS)
        data = response.json()
        self.destination_data = data['prices']
        pprint(self.destination_data)
        return self.destination_data


    def update_destination_codes(self):
        for city in  self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city['iataCode'],
                }
            }
            response = requests.put(url=f"{ENDPOINT}/{city['id']}", json=new_data, headers=HEADERS)
            print(response.text)

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/13eea4da04d7a3ea3019f72c28082354/flightDeals/users"
        HEADERS = {"Authorization": f"Bearer SWANFLY"}
        response = requests.get(customers_endpoint, headers=HEADERS)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
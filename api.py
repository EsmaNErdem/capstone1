import os
import requests
from datetime import datetime, timedelta


api_key = os.getenv('API_KEY')
BASE_URL = 'https://developer.nps.gov/api/v1'

class Alerts():
    """Alerts class model to create fundtion to make API requests"""

    def get_response(self):
        """Makes API request to get recetns alerts."""

        response = requests.get(f'{BASE_URL}/alerts',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    

class Centers():
    """Centers class model to create fundtion to make API requests"""

    def get_response(self):
        """Makes API request to get visitor center locations."""

        response = requests.get(f'{BASE_URL}/visitorcenters',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    
class Info():
    """Info class model to create fundtion to make API requests"""

    def get_response(self):
        """Makes API request to get info about ANP."""

        response = requests.get(f'{BASE_URL}/parks',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    
class Activities():
    """Activity model to create fundtion to make API requests"""

    def get_response(self):
        """Makes API request to get list of activities."""

        response = requests.get(f'{BASE_URL}/thingstodo',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    
    def get_activity(self, id):
        """Makes API request to get selected activity data."""

        response = requests.get(f'{BASE_URL}/thingstodo',
                                params={"parkCode": "acad",
                                        "id": id,
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    

class Events():
    """Events Model Class to functions to make event related API calls"""

    def get_response(self):
        """Makes API request to get list of events."""

        now = datetime.utcnow()
        today = now.strftime('%Y-%m-%d')
        # API doesn't take any other date other than 2023-01-01 but it wasn't like this first. 
        # Take a look why???????????

        response = requests.get(f'{BASE_URL}/events',
                                params={"parkCode": "acad",
                                        "dateStart": "2023-01-01",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    

class Places():
    """Places model class to create function to places API calls"""

    def get_response(self):
        """Makes API request to get list of places."""

        response = requests.get(f'{BASE_URL}/places',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    
    def get_place(self, id):
        """Makes API request to get selected place data."""

        response = requests.get(f'{BASE_URL}/places',
                                params={"parkCode": "acad",
                                        "id": id,
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
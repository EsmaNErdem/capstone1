import os
import requests

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
    """Info Activity model to create fundtion to make API requests"""

    def get_response(self):
        """Makes API request to get list of activities."""

        response = requests.get(f'{BASE_URL}/thingstodo',
                                params={"parkCode": "acad",
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    
    def get_activity(self, id):
        """Makes API request to get list of activities."""

        response = requests.get(f'{BASE_URL}/thingstodo',
                                params={"parkCode": "acad",
                                        "id": id,
                                        "api_key": api_key}
                            )
        data = response.json()
        return data['data']
    

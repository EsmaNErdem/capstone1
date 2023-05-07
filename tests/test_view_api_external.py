"""External API call page show tests"""

#    FLASK_ENV=production python -m unittest tests/test_view_api_external.py

import os
from unittest import TestCase
from models import db, User
from api import Activities
from api import Alerts, Centers, Info, Activities, Events, Places
from unittest.mock import patch

os.environ['DATABASE_URL'] = "postgresql:///wicked_test"
from app import app, CURR_USER_KEY

db.create_all()

class ApiCallTestCase(TestCase):
    """Tests external API Call Respond View Pages"""

    def setUp(self):
        """Create test client, add sample data."""

        os.environ['DATABASE_URL'] = "postgresql:///wicked-test"
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True
        self.client = app.test_client()

        db.drop_all()
        db.create_all()

        user = User.signup(
            email='user1@example.com',
            username='user1',
            password='password123',
            first_name='userfirst',
            last_name='userlast',
            image_url=None, 
            reset_token= None
        )

        db.session.commit()

        user = User.query.filter_by(username='user1').one()
        self.user = user

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_activities_view(self):
        """Testing list of activities view page by mocking external API call data"""

        with patch('app.activities.get_response') as mock_get_response:
            mock_activities = [
                {'id': 1, 'title': 'Activity 1', 'description': 'Description 1', 'images': [{'crops':[{'url':'Image 1'}], 'caption':'Caption'}]},
                {'id': 2, 'title': 'Activity 2', 'description': 'Description 2', 'images': [{'crops':[{'url':'Image 2'}], 'caption':'Caption'}]},
                {'id': 3, 'title': 'Activity 3', 'description': 'Description 3', 'images': [{'crops':[{'url':'Image 3'}], 'caption':'Caption'}]}
            ]
            mock_get_response.return_value = mock_activities
            
            response = self.client.get('/activities')
            html = response.get_data(as_text=True)
            
            for activity in mock_activities:
                self.assertIn(activity['title'], html)
                self.assertIn(activity['images'][0]['crops'][0]['url'], html)

    def test_activity_view(self):
        """Testing activity view page by mocking external API call data"""

        with patch('app.activities.get_activity') as mock_get_activity:
            mock_activity = [
                {'id': 1, 'title': 'Activity 1', 'activities':[{"name": "Name 1"}], 'seasonDescription': 'Description 1', 'accessibilityInformation':'data', 'ageDescription':'data', 'petsDescription':'data', 'durationDescription':'data', 'activityDescription':'data', 'longDescription':'data', 'images': [{'crops':[{'url':'Image 1'}], 'caption':'Caption'}]},
            ]
            mock_get_activity.return_value = mock_activity
            
            response = self.client.get('/activities/1')
            html = response.get_data(as_text=True)
            
            self.assertIn(mock_activity[0]['ageDescription'], html)
            self.assertIn(mock_activity[0]['images'][0]['crops'][0]['url'], html)

    
    def test_events_view(self):
        """Testing list of events view page by mocking external API call data"""

        with patch('app.events.get_response') as mock_get_response:
            mock_events = [
                {'id': 1, 'title': 'Event 1', 'description': 'Description 1', 'regresinfo': 'Regresinfo 1', 'contactname':'Contactname 1', 'types':' Type 1'},
                {'id': 2, 'title': 'Event 2', 'description': 'Description 2', 'regresinfo': 'Regresinfo 2', 'contactname':'Contactname 2', 'types':'Type 2'},
                {'id': 3, 'title': 'Event 3', 'description': 'Description 3', 'regresinfo': 'Regresinfo 3', 'contactname':'Contactname 3', 'types':'Type 3'},
            ]
            mock_get_response.return_value = mock_events
            
            response = self.client.get('/events')
            html = response.get_data(as_text=True)
            
            for event in mock_events:
                self.assertIn(event['title'], html)
                self.assertIn(event['description'], html)


    def test_places_view(self):
        """Testing list of places view page by mocking external API call data"""

        with patch('app.places.get_response') as mock_get_response:
            mock_places = [
                {'id': 1, 'title': 'Place 1', 'audioDescription': 'Description 1', 'images': [{'crops':[{'url':'Image 1'}], 'title':'Caption'}]},
                {'id': 2, 'title': 'Place 2', 'audioDescription': 'Description 2', 'images': [{'crops':[{'url':'Image 2'}], 'title':'Caption'}]},
                {'id': 3, 'title': 'Place 3', 'audioDescription': 'Description 3', 'images': [{'crops':[{'url':'Image 3'}], 'title':'Caption'}]},
            ]
            mock_get_response.return_value = mock_places
            
            response = self.client.get('/places')
            html = response.get_data(as_text=True)
            
            for place in mock_places:
                self.assertIn(place['title'], html)
                self.assertIn(place['audioDescription'], html)

    def test_place_view(self):
        """Testing place view page by mocking external API call data"""

        with patch('app.places.get_place') as mock_get_place:
            mock_place = [
                {'id': 1, 'title': 'Place 1', 'listingDescription': 'Description 1', 'images': [{'crops':[{'url':'Image 1'}], 'title':'Caption', 'caption':'Caption'}], 'bodyText': 'Placebody 1'}
            ]
            mock_get_place.return_value = mock_place
            
            response = self.client.get('/places/1')
            html = response.get_data(as_text=True)
            
            self.assertIn(mock_place[0]['listingDescription'], html)
            self.assertIn(mock_place[0]['images'][0]['crops'][0]['url'], html)

            





           

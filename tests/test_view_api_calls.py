"""Restful API tests"""

#    FLASK_ENV=production python -m unittest tests/test_view_api_calls.py

import os
from unittest import TestCase
from models import db, User
from api import Alerts, Centers, Info, Activities, Events, Places

os.environ['DATABASE_URL'] = "postgresql:///wicked_test"

from app import app, CURR_USER_KEY

db.create_all()

class ApiCallTestCase(TestCase):
    """Tests API Call Respond View Pages"""

    def setUp(self):
        """Create test client, add sample data."""

        os.environ['DATABASE_URL'] = "postgresql:///wicked-test"
        app.config['SQLALCHEMY_ECHO'] = False
        # os.environ['API_KEY'] = os.getenv('API_KEY')
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
    
    def test_homapage(self):
        """Test restful API route to add  a new activity to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
                os.getenv('API_KEY')

            # resp = c.get("/activities")
            activities = Activities()

            import pdb
            pdb.set_trace()
            act = activities.get_response()

            
# (Pdb) infor


# API KEY IS MISSING WHEN THE API CALLS ARE IN TERMINAL OR TESTING ANYWHERE OUTSIDE OF FLASK RUN, SO FAR!!! WHY???? OS.ENV CANNOT GET THE API_KEY? HOW TO FIX IT?
# {'error': {'code': 'API_KEY_MISSING', 'message': 'An API key was not provided. Please get one at https://www.nps.gov/subjects/developer/get-started.htm'}}



           

"""Restful API tests"""

#    FLASK_ENV=production python -m unittest tests/test_restful_api.py

import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Activity

os.environ['DATABASE_URL'] = "postgresql:///wicked_test"

from app import app, CURR_USER_KEY

db.create_all()

ACTIVITY_DATA = {
    "id" : "ActivityId",
    "title" : "Title",
    "description" : "Content",
    "imageUrl" : "Image"
}
EVENT_DATA = {
    "id" : "EventId",
    "title" : "Title",
    "description" : "Content",
}
PLACE_DATA = {
    "id" : "PlaceId",
    "title" : "Title",
    "description" : "Content",
    "imageUrl" : "Image"
}

class RestfulApiTestCase(TestCase):
    """Tests Restful API Routes"""

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

        activity1 = Activity(id="activity1", title="title", description="test-desc", image_url="test")

        db.session.add(activity1)
        db.session.commit()

        self.activity = activity1


    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res   
    
    def test_favorite_activity_new(self):
        """Test restful API route to add  a new activity to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/favorite", json=ACTIVITY_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.fav_activities), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Favorite"
            })

    def test_favorite_activity(self):
        """Test restful API route to add activity that's already in the database to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/favorite", json={"id" : self.activity.id })

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.fav_activities), 1)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Favorite"
                })
            
    def test_favorite_activity_fail (self):
        """Test restful API route to  fail adding activity that's already in the user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/favorite", json={"id" : self.activity.id })
            resp= c.post("/api/activity/favorite", json=ACTIVITY_DATA)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.fav_activities), 2)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Favorite"
                })   
            
        with self.assertRaises(IntegrityError):
            c.post("/api/activity/favorite", json={"id" : self.activity.id })


    def test_favorite_event(self):
        """Test restful API route to add a new event to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/event/favorite", json=EVENT_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.fav_events), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Favorite"
            })
        
    def test_favorite_place(self):
        """Test restful API route to add a new place to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/place/favorite", json=PLACE_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.fav_places), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Favorite"
            })

# BOOKMARK
    def test_bookmark_activity_new(self):
        """Test restful API route to add  a new activity to user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/bookmark", json=ACTIVITY_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.marked_activities), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Bookmark"
            })

    def test_bookmark_activity(self):
        """Test restful API route to add activity that's already in the database to user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/bookmark", json={"id" : self.activity.id })

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.marked_activities), 1)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Bookmark"
                })
            
    def test_bookmark_activity_fail (self):
        """Test restful API route to  fail adding activity that's already in the user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/activity/bookmark", json={"id" : self.activity.id })
            resp= c.post("/api/activity/bookmark", json=ACTIVITY_DATA)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.marked_activities), 2)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Bookmark"
            })   
            
        with self.assertRaises(IntegrityError):
            c.post("/api/activity/bookmark", json={"id" : self.activity.id })

    def test_bookmark_event(self):
        """Test restful API route to add a new event to user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/event/bookmark", json=EVENT_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.marked_events), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Bookmark"
        })
        
    def test_bookmark_place(self):
        """Test restful API route to add a new place to user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/place/bookmark", json=PLACE_DATA)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.user.marked_places), 1)

        data = resp.json
        self.assertEqual(data, {
            "message": "Added to Bookmark"
        })
        

# DELETE favorite and bookmark
    def test_favorite_event_delete(self):
        """Test restful API route to add a new event to user favorite list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/event/favorite", json=EVENT_DATA)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.fav_events), 1)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Favorite"
            })
            
            response_delete = c.delete(f"/api/event/{self.user.fav_events[0].id}/favorite")

            self.assertEqual(response_delete.status_code, 200)
            self.assertEqual(len(self.user.fav_events), 0)

            data = response_delete.json
            self.assertEqual(data, {
                "message": "Deleted"
            })
        
    
    def test_bookmark_place_delete(self):  
        """Test restful API route to add a new place to user bookmark list"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp= c.post("/api/place/bookmark", json=PLACE_DATA)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.user.marked_places), 1)

            data = resp.json
            self.assertEqual(data, {
                "message": "Added to Bookmark"
            })
            
            response_delete = c.delete(f"/api/place/{self.user.marked_places[0].id}/bookmark")

            self.assertEqual(response_delete.status_code, 200)
            self.assertEqual(len(self.user.marked_places), 0)

            data = response_delete.json
            self.assertEqual(data, {
                "message": "Deleted"
            })
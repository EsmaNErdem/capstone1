"""User View tests."""


#    FLASK_ENV=production python -m unittest tests/test_user_view.py


import os
from unittest import TestCase

from models import db, connect_db, User, Activity, Event, Place, Favorite, Bookmark

os.environ['DATABASE_URL'] = "postgresql:///wicked_test"

from app import app, CURR_USER_KEY

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Test views for user profile and user related data"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

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

        activity1 = Activity(id="activity1", title="title", description="activity1", image_url="test")
        activity2 = Activity(id="activity2", title="title", description="test-desc", image_url="test")
        event = Event(id="event1", title="title", description="test-desc")
        place1 = Place(id="place1", title="title", description="place1", image_url="test")
        place2 = Place(id="place2", title="title", description="test-desc", image_url="test")

        db.session.add_all([activity1, activity2, event, place1, place2])
        db.session.commit()

        fav_events = Favorite(user_id = user.id, event_id = event.id)
        fav_activity1 = Favorite(user_id = user.id, activity_id = activity1.id)
        fav_activity2 = Favorite(user_id = user.id, activity_id = activity2.id)
        
        db.session.add_all([fav_events, fav_activity1, fav_activity2])
        db.session.commit()

        marked_events = Bookmark(user_id = user.id, event_id = event.id)
        marked_place1 = Bookmark(user_id = user.id, place_id = place1.id)
        marked_place2 = Bookmark(user_id = user.id, place_id = place2.id)

        db.session.add_all([marked_events, marked_place1, marked_place2])
        db.session.commit()

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res        

    def test_user_profile(self):
        """Test view user profile"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.username, str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<i class="fa-solid fa-heart favorite"></i>Favorites', html)
            self.assertIn('<i class="fa-solid fa-bookmark bookmark"></i>Bookmarks</a>', html)

    def test_user_profile_edit(self):
        """Test view user profile edit"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/edit")

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('<button class="btn btn-success">Edit this user!</button>', html)
            

            resp = c.post(f"/users/{self.user.id}/edit", data={
                "username": "new_username",
                "email": "new@email.com"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("new_username", str(resp.data))
            self.assertIn("new@email.com", str(resp.data))

    def test_user_profile_edit_unauthenticated(self):
        """Test view user fail profile edit without authentication"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get("/users/9999/edit", follow_redirects=True)


            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))


    def test_user_profile_delete(self):
        """Test view user profile delete"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.post("/users/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
        
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Sign Up</h1>', html)

    def test_user_search(self):
        """Tests user favorite and bookmark search"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
                
            resp = c.get("/search?q=title")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.user.fav_activities[0].title, str(resp.data))
            self.assertIn(self.user.marked_events[0].title, str(resp.data))
            self.assertIn('place1', str(resp.data))


    def test_user_favorites(self):
        """Test view user favorites"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/favorites")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('1 - Events', str(resp.data))
            self.assertIn('2 - Activities', str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Favorites</h1>', html)

    def test_user_favorite_activities(self):
        """Test view user favorites activities"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/favorites/activities")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('1 - Events', str(resp.data))
            self.assertIn(self.user.fav_activities[0].title, str(resp.data))
            self.assertIn(self.user.fav_activities[1].title, str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Favorites</h1>', html)

    def test_user_favorite_events(self):
        """Test view user favorite events"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/favorites/events")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('2 - Activities', str(resp.data))
            self.assertIn(self.user.fav_events[0].title, str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Favorites</h1>', html)


    def test_user_bookmarks(self):
        """Test view user bookmarks"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/bookmarks")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('1 - Events', str(resp.data))
            self.assertIn('2 - Places', str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Bookmarks</h1>', html)


    def test_user_bookmark_places(self):
        """Test view user bookmark places"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/bookmarks/places")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('1 - Events', str(resp.data))            
            self.assertIn(self.user.marked_places[0].title, str(resp.data))
            self.assertIn(self.user.marked_places[1].title, str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Bookmarks</h1>', html)


    def test_user_bookmark_events(self):
        """Test view user bookmarks events"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/bookmarks/events")

            self.assertEqual(resp.status_code, 200)

            self.assertIn('1 - Events', str(resp.data))            
            self.assertIn(self.user.marked_events[0].title, str(resp.data))
            html = resp.get_data(as_text=True)
            self.assertIn('<h1 class="display-1">Bookmarks</h1>', html)


           
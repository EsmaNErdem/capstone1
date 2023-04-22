"""User model tests."""

#    python -m unittest tests/test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Activity, Event, Place, Favorite, Bookmark


os.environ['DATABASE_URL'] = "postgresql:///wicked_test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
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


    def test_user_model(self):
        """Does basic model work?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            first_name='userfirst',
            last_name='userlast', 
            image_url=None, 
            reset_token= None
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.marked_events), 0)
        self.assertEqual(len(u.fav_events), 0)


    def test_user_signup(self):
        """Test users with correct credentials can sign up properly."""
        
        user1 = User.signup(username='testuser', email='testuser@example.com', password='password', first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)
        db.session.add(user1)
        db.session.commit()
        
        user = User.query.filter_by(username='testuser').one()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertNotEqual(user.password, 'password')
        self.assertTrue(user.password.startswith('$2b$'))

    def test_invalid_user_signup(self):
        """Test users with incorrect credentials cannot sign up properly."""

        with self.assertRaises(ValueError):
            User.signup(username='testuser', email='testuser@example.com', password=None, first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)


    def test_invalid_username(self):
        """Tests users fialing to signup with an username"""

        with self.assertRaises(IntegrityError):
            User.signup(username=None, email='testuser@example.com', password='password', first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)
            db.session.commit()

    def test_invalid_email(self):
        """Tests users faiiling to signup without an email"""

        with self.assertRaises(IntegrityError):
            User.signup(username='testuser', email=None, password='password', first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)
            db.session.commit()

    def test_invalid_first_name(self):
        """Tests users faiiling to signup without a firstname"""

        with self.assertRaises(IntegrityError):
            User.signup(username='testuser', email='testuser@example.com', password='password', first_name=None, last_name='userlast', image_url=None, reset_token= None)
            db.session.commit()
        
    def test_invalid_lastname(self):
        """Tests users faiiling to signup without a lastname"""

        with self.assertRaises(IntegrityError):
            User.signup(username='testuser', email='testuser@example.com', password='password', first_name='userfirst', last_name=None, image_url=None, reset_token= None)
            db.session.commit()

    def test_unique_email_error(self):
        """Test that a user with the same email cannot be added again."""
        
        user1 = User.signup(username='testuser1', email='testuser@example.com', password='password',first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)
        db.session.add(user1)
        db.session.commit()
        
        user2 = User.signup(username='testuser2', email='testuser@example.com', password='password', first_name='userfirst', last_name='userlast', image_url=None, reset_token= None)
        with self.assertRaises(IntegrityError):
            db.session.add(user2)
            db.session.commit()

    def test_valid_authentication(self):
        """Tests User model classmethod to login user"""

        u = User.authenticate(self.user.username, "password123")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.user.id)
    
    def test_invalid_username(self):
        """Tests user authentication with an invalid name"""

        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        """Tests user authentication with an invalid password"""

        self.assertFalse(User.authenticate(self.user.username, "badpassword"))

    def test_user_adding_favorites(self):
        """Test users adding data to their favorites table"""

        activity1 = Activity(id="activity1", title="title", description="test-desc", image_url="test")
        activity2 = Activity(id="activity2", title="title", description="test-desc", image_url="test")
        event = Event(id="event1", title="title", description="test-desc")
        
        db.session.add_all([activity1, activity2, event])
        db.session.commit()

        fav_events = Favorite(user_id = self.user.id, event_id = event.id)
        fav_activity1 = Favorite(user_id = self.user.id, activity_id = activity1.id)
        fav_activity2 = Favorite(user_id = self.user.id, activity_id = activity2.id)
        
        db.session.add_all([fav_events, fav_activity1, fav_activity2])
        db.session.commit()

        self.assertEqual(len(self.user.fav_activities), 2)
        self.assertEqual(len(self.user.fav_events), 1)

    def test_user_adding_bookmarks(self):
        """Test users adding data to their bookmarks table"""

        event = Event(id="event1", title="title", description="test-desc")
        place1 = Place(id="place1", title="title", description="test-desc", image_url="test")
        place2 = Place(id="place2", title="title", description="test-desc", image_url="test")

        db.session.add_all([event, place1, place2])
        db.session.commit()

        marked_events = Bookmark(user_id = self.user.id, event_id = event.id)
        marked_place1 = Bookmark(user_id = self.user.id, place_id = place1.id)
        marked_place2 = Bookmark(user_id = self.user.id, place_id = place2.id)

        db.session.add_all([marked_events, marked_place1, marked_place2])
        db.session.commit()

        self.assertEqual(len(self.user.marked_places), 2)
        self.assertEqual(len(self.user.marked_events), 1)



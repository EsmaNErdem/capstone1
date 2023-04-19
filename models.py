from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connecting the database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    marked_places = db.relationship(
        'Place',
        secondary='bookmarks',
        backref='users_mark_place'
    )
    
    marked_events = db.relationship(
        'Event',
        secondary='bookmarks',
        backref='users_mark_event'
    )

    marked_activities = db.relationship(
        'Activity',
        secondary='bookmarks',
        backref='users_mark_act'
    )

    @property
    def get_full_name(self):
        """Return users fullname"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, first_name, last_name, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


# -------------------------create class function to change password, 


class Activity(db.Model):
    """Activity database Model Class to save data"""

    __tablename__ = 'activities'

    id = db.Column(
        db.Text,
        primary_key=True,
    )

    image_url = db.Column(
        db.Text,
    )

    title = db.Column(
        db.Text,
    )

    description = db.Column(
        db.Text,
    )

    users_fav= db.relationship(
        'User',
        secondary='favorites',
        backref='fav_activities'
    )


class Event(db.Model):
    """Event database Model Class to save data"""

    __tablename__ = 'events'

    id = db.Column(
        db.Text,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
    )

    description = db.Column(
        db.Text,
    )

    users_fav_event = db.relationship(
        'User',
        secondary='favorites',
        backref='fav_events'
    )

class Place(db.Model):
    """Place database Model Class to save data"""

    __tablename__ = 'places'

    id = db.Column(
        db.Text,
        primary_key=True,
    )

    image_url = db.Column(
        db.Text,
    )

    title = db.Column(
        db.Text,
    )

    description = db.Column(
        db.Text,
    )

    users_fav_place = db.relationship(
        'User',
        secondary='favorites',
        backref='fav_places'
    )

class Favorite(db.Model):
    """Mapping user favorite"""

    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False,
    )

    place_id = db.Column(
        db.Text,
        db.ForeignKey('places.id', ondelete='cascade'),
    )

    event_id = db.Column(
        db.Text,
        db.ForeignKey('events.id', ondelete='cascade'),
    )
    
    activity_id = db.Column(
        db.Text,
        db.ForeignKey('activities.id', ondelete='cascade'),
    )


class Bookmark(db.Model):
    """Mapping user favorite"""

    __tablename__ = 'bookmarks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False,
    )

    place_id = db.Column(
        db.Text,
        db.ForeignKey('places.id', ondelete='cascade'),
    )

    event_id = db.Column(
        db.Text,
        db.ForeignKey('events.id', ondelete='cascade'),
    )
    
    activity_id = db.Column(
        db.Text,
        db.ForeignKey('activities.id', ondelete='cascade'),
    )
    

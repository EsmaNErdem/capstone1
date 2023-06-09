from models import db, User, Activity, Place, Event, Favorite, Bookmark
from app import app
from flask import session

# Create all tables
db.drop_all()
db.create_all()
db.session.close()
# if table isn't empy, empty it
# User.query.delete()
# Activity.query.delete()
# Place.query.delete()
# Event.query.delete()
# Favorites.query.delete()
# Bookmark.query.delete()

# User instances
mike = User.signup(username='MikeB', email='testuser1@example.com', password='password', first_name='Mike', last_name='Baker', image_url='https://i.pinimg.com/736x/1b/9a/26/1b9a26a9093f63773bd7c2d54f26bbd2--funny-stuff-google-search.jpg', reset_token=None)
esma = User.signup(username='EsmaB', email='testuser2@example.com', password='password', first_name='Esma', last_name='Erdem', image_url='https://hips.hearstapps.com/hmg-prod/images/dog-jokes-1581711487.jpg?crop=0.684xw:1.00xh;0.274xw,0&resize=1200:*', reset_token=None)
smokey = User.signup(username='SmokeyB', email='testuser3@example.com', password='password', first_name='Smokey', last_name='Kittiler', image_url='https://thumbs.dreamstime.com/b/funny-close-up-portrait-tabby-maine-coon-cat-194565488.jpg', reset_token=None)

db.session.add_all([mike, esma, smokey])
db.session.commit()

# Activity instances
act1 = Activity(id='Iamalonglongidtext4', title='acadia1', description='test1')
act2 = Activity(id='Iamalonglongidtext5', title='acadia2', description='test2')

db.session.add_all([act1, act2])
db.session.commit()

# Place instances
place1 = Place(id='Iamalonglongidtext6', title='acadia1', description='test1')
place2 = Place(id='Iamalonglongidtext7', title='acadia2', description='test2')

db.session.add_all([place1, place2])
db.session.commit()

# Event instance
event1 = Event(id='Iamalonglongidtext8', title='acadia1', description='test1')
event2 = Event(id='Iamalonglongidtext9', title='acadia2', description='test2')

db.session.add_all([event1, event2])
db.session.commit()

fav_event = Favorite(user_id=mike.id, event_id=event2.id)
db.session.add_all([fav_event])
db.session.commit()

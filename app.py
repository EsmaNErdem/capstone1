import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import Pagination

from forms import UserSignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from models import db, connect_db, User, Activity, Event, Place, Favorite, Bookmark
from api import Alerts, Centers, Info, Activities, Events, Places

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///wicked_acadia'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "this is my key")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
app.app_context().push()
connect_db(app)

alerts = Alerts()
centers = Centers()
info = Info()
activities = Activities()
events = Events()
places = Places()

from flask_mail import Mail, Message
import secrets

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'wickedacadia40@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'wickedacadia40@gmail.com'

mail = Mail(app)

# ------------USER ROUTES---------------#
# SIGNUP/LOGIN/LOGOUT

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user, remember ):
    """Log in user by saving user_id in session"""

    session[CURR_USER_KEY] = user.id
    if remember:
        session.permanent = True


def do_logout():
    """Logout user by removing user_is from session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    if g.user:
        return redirect(f"/users/{g.user.id}")
    
    form = UserSignUpForm()

    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                reset_token= None,
            )
            db.session.commit()
            
        except IntegrityError:
            flash("Invalid username, please try again", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user, remember=False)

        return redirect(url_for('profile', user_id=user.id))

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Show login form and authenticate user"""

    if g.user:
        return redirect(f"/users/{g.user.id}")
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        remember = request.form.get('remember')

        if user:
            do_login(user, remember=remember)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You logged out.", "success")
    return redirect('/login')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Sends user a token to start reset password process"""

    if g.user:
        return redirect(f"/users/{g.user.id}")
    
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_hex(16)
            user.reset_token = token
            db.session.commit()
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'''To reset your password, please visit the following link:

            {reset_url}

            If you did not make this request then simply ignore this email and no changes will be made.

            Wicked Acadia sends her regards!
            '''
            try: 
                mail.send(msg)
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                flash("Failed, please try again", 'danger')
                return render_template(url_for('forgot_password'))  
        else:
            flash("No account found with this email, please try again", 'danger')
            return render_template('/users/forgot-psw.html', form=form)  
           
    return render_template('/users/forgot-psw.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """"""

    user = User.query.filter_by(reset_token=token).first()
    
    if not user:
        flash('Invalid or expired token. Please try again.', 'danger')
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()

    if request.method == 'POST':
        new_password = form.new_password.data
        user = User.reset(user, new_password)

        db.session.commit()
        flash('Your password has been reset. You can now log in with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('users/reset.html', form=form)

# USER PROFILE ROUTES

@app.route('/users/<int:user_id>')
def profile(user_id):
    """Show user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)
    
    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Show user edit form and update user data"""

    if g.user.id != user_id or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = g.user

    form =  UserSignUpForm(obj = user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.image_url = form.image_url.data

            db.session.commit()
            flash(f"{user.username}'s profile has been updated.", "success")
            return redirect(url_for('profile', user_id=user.id))
        else: 
            flash("Please enter correct password to confirm.", "danger")
    return render_template('users/edit.html', form=form)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

# User-Favorites

@app.route('/users/<int:user_id>/favorites')
def user_favorite(user_id):
    """Show user favorites."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")

    user = User.query.get_or_404(user_id)
    activity_fav = g.user.fav_activities
    event_fav = g.user.fav_events
    place_fav = g.user.fav_places
    
    return render_template('users/favorites/favorites.html', user=user, activities=activity_fav, events=event_fav, places=place_fav)

@app.route('/users/<int:user_id>/favorites/activities')
def user_favorite_activities(user_id):
    """Show user activities favorites."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    activity_fav = g.user.fav_activities
    event_fav = g.user.fav_events
    place_fav = g.user.fav_places
    activity_ids_fav = [activity.id for activity in g.user.fav_activities]
    activity_ids_mark = [activity.id for activity in g.user.marked_activities]

    return render_template('users/favorites/fav-activity.html', user=user, activities=activity_fav, events=event_fav, places=place_fav, activity_ids_fav=activity_ids_fav, activity_ids_mark=activity_ids_mark)

@app.route('/users/<int:user_id>/favorites/events')
def user_favorite_events(user_id):
    """Show user events favorites."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    activity_fav = g.user.fav_activities
    event_fav = g.user.fav_events
    place_fav = g.user.fav_places
    event_ids_fav = [event.id for event in g.user.fav_events]
    event_ids_mark = [event.id for event in g.user.marked_events]    

    return render_template('users/favorites/fav-event.html', user=user, events=event_fav, activities=activity_fav, places=place_fav, event_ids_fav=event_ids_fav, event_ids_mark=event_ids_mark)

@app.route('/users/<int:user_id>/favorites/places')
def user_favorite_places(user_id):
    """Show user places favorites."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    place_fav = g.user.fav_places    
    activity_fav = g.user.fav_activities
    event_fav = g.user.fav_events
    place_ids_fav = [place.id for place in g.user.fav_places]
    place_ids_mark = [place.id for place in g.user.marked_places]

    return render_template('users/favorites/fav-place.html', user=user, places=place_fav, events=event_fav, activities=activity_fav, place_ids_fav=place_ids_fav, place_ids_mark=place_ids_mark)

# User-Bookmarks

@app.route('/users/<int:user_id>/bookmarks')
def user_bookmark(user_id):
    """Show user bookmarks."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")

    user = User.query.get_or_404(user_id)
    activity_mark = g.user.marked_activities
    event_mark = g.user.marked_events
    place_mark = g.user.marked_places
    
    return render_template('users/bookmarks/bookmarks.html', user=user, activities=activity_mark, events=event_mark, places=place_mark)

@app.route('/users/<int:user_id>/bookmarks/activities')
def user_bookmark_activities(user_id):
    """Show user activities bookmarks."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    activity_mark = g.user.marked_activities
    event_mark = g.user.marked_events
    place_mark = g.user.marked_places
    activity_ids_mark = [activity.id for activity in g.user.marked_activities]
    activity_ids_fav = [activity.id for activity in g.user.fav_activities]


    return render_template('users/bookmarks/mark-activity.html', user=user, activities=activity_mark, events=event_mark, places=place_mark, activity_ids_mark=activity_ids_mark, activity_ids_fav=activity_ids_fav)

@app.route('/users/<int:user_id>/bookmarks/events')
def user_bookmark_events(user_id):
    """Show user events bookmarks."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    activity_mark = g.user.marked_activities
    event_mark = g.user.marked_events
    place_mark = g.user.marked_places
    event_ids_mark = [event.id for event in g.user.marked_events]

    return render_template('users/bookmarks/mark-event.html', user=user, events=event_mark, activities=activity_mark, places=place_mark, event_ids_mark=event_ids_mark)

@app.route('/users/<int:user_id>/bookmarks/places')
def user_bookmark_places(user_id):
    """Show user places bookmarks."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.id != user_id:
        return redirect(f"/users/{g.user.id}")
    
    user = User.query.get_or_404(user_id)    
    place_mark = g.user.marked_places    
    activity_mark = g.user.marked_activities
    event_mark = g.user.marked_events
    place_ids_mark = [place.id for place in g.user.marked_places]
    place_ids_fav = [place.id for place in g.user.fav_places]

    return render_template('users/bookmarks/mark-place.html', user=user, places=place_mark, events=event_mark, activities=activity_mark, place_ids_mark=place_ids_mark, place_ids_fav=place_ids_fav)


# ----------------ACTIVITIES---------------
         

@app.route('/activities')
def show_activities():
    """Shows list of activities with short description"""

    
    try: 
        activities_data = activities.get_response()
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    if not g.user:
        return render_template('activities/list.html', activities=activities_data)
    

    # page = int(request.args.get('page', 1))
    # per_page = 20 
    # offset = (page - 1) * per_page 
    # items_pagination = activities_data[offset:offset+per_page] 
    # total = len(activities_data) 
    # pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total) 
    # , pagination=pagination



#     File "/home/esma/springboard/capstone1/app.py", line 424, in show_activities
#     pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total)
#   File "/home/esma/springboard/capstone1/venv/lib/python3.10/site-packages/flask_sqlalchemy/pagination.py", line 69, in __init__
#     items = self._query_items()
#   File "/home/esma/springboard/capstone1/venv/lib/python3.10/site-packages/flask_sqlalchemy/pagination.py", line 156, in _query_items
#     raise NotImplementedError
# NotImplementedError

    activity_ids_fav = [activity.id for activity in g.user.fav_activities]
    activity_ids_mark = [activity.id for activity in g.user.marked_activities]

    return render_template('activities/list.html', activities=activities_data, activity_ids_fav=activity_ids_fav, activity_ids_mark=activity_ids_mark)

@app.route('/activities/<activity_id>')
def show_activity(activity_id):
    """Shows selected Activity with detailed info"""

    try: 
        activity_data = activities.get_activity(activity_id)
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    if not g.user:
        return render_template('activities/show.html', activity=activity_data[0])

    favored = Activity.query.get(activity_id) in g.user.fav_activities
    marked = Activity.query.get(activity_id) in g.user.marked_activities

    return render_template('activities/show.html', activity=activity_data[0], favored=favored, marked=marked)


# ------------------EVENTS-------------------

@app.route('/events')
def show_events():
    """Shows list of events with short description"""
    
    try: 
        events_data = events.get_response()
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    if not g.user:
        return render_template('events/list.html', events=events_data,)
    
    event_ids_fav = [event.id for event in g.user.fav_events]
    event_ids_mark = [event.id for event in g.user.marked_events]

    return render_template('events/list.html', events=events_data, event_ids_fav=event_ids_fav, event_ids_mark=event_ids_mark)


# ---------------PLACES-----------------

@app.route('/places')
def show_places():
    """Shows list of places with short description"""
    
    try: 
        places_data = places.get_response()
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')  
    
    if not g.user:
        return render_template('places/list.html', places=places_data)    
      
    place_ids_fav = [place.id for place in g.user.fav_places]
    place_ids_mark = [place.id for place in g.user.marked_places]
   
    return render_template('places/list.html', places=places_data, place_ids_fav=place_ids_fav, place_ids_mark=place_ids_mark)

@app.route('/places/<place_id>')
def show_place(place_id):
    """Shows selected place with detailed info"""
    
    try: 
        place_data = places.get_places(place_id)
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    if not g.user:
        return render_template('places/show.html', place=place_data[0])
        
    favored = Place.query.get(place_id) in g.user.fav_places
    marked = Place.query.get(place_id) in g.user.marked_places

    return render_template('places/show.html', place=place_data[0], favored=favored, marked=marked)

# ------------------HOMEPAGE------------
# Homepage and Error Pages

@app.route('/')
def show_homepage_info():
    """Show homepge anf info about about Acadia National Park"""

    try: 
        info_data = info.get_response()
    except Exception as e:
        print(f"API Error****************************: {e}") 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    return render_template('homepage/info.html', info=info_data[0])

@app.route('/alerts')
def show_alerts():
    """Show alerts"""

    try:
        info_data = info.get_response()
        alerts_data = alerts.get_response() 
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    return render_template('homepage/alerts.html', alerts=alerts_data, info=info_data[0])

@app.route('/centers')
def show_centers():
    """Show visitor centers"""

    try:
        centers_data = centers.get_response()
        info_data = info.get_response()
    except: 
        flash("There was an API error. Pleace try again later", 'danger')
        return render_template('homepage/api-error.html')
    
    return render_template('homepage/visitor-center.html', centers=centers_data, info=info_data[0])

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_authorized(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 401


# -----------------Restful API Routes-------------------

# Activity
@app.route("/api/activity/favorite", methods=["POST"])
def add_fav_act():
    """Creates Activity instance and adds it to user's fav list"""
    
    id = request.json['id']

    if not Activity.query.get(id):
        activity = Activity(
            id = request.json['id'],
            image_url = request.json['imageUrl'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(activity)
        db.session.commit()
    else: 
        activity = Activity.query.get(id) 
    
    fav_activities = Favorite(
        user_id = g.user.id,
        activity_id = activity.id
    )
    db.session.add(fav_activities)
    db.session.commit()

    return (jsonify(message="Added to Favorite"))

@app.route("/api/activity/<activity_id>/favorite", methods=["DELETE"])
def remove_fav_act(activity_id):
    """Removes from activity from user favorite and from database"""

    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    g.user.fav_activities.remove(activity)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route("/api/activity/bookmark", methods=["POST"])
def add_mark_act():
    """Creates Activity instance and adds it to user's bookmark list"""

    id = request.json['id']
    
    if not Activity.query.get(id):
        activity = Activity(
            id = request.json['id'],
            image_url = request.json['imageUrl'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(activity)
        db.session.commit()
    else: 
        activity = Activity.query.get(id) 
    
    mark_activities = Bookmark(
        user_id = g.user.id,
        activity_id = activity.id
    )
    db.session.add(mark_activities)
    db.session.commit()

    return (jsonify(message="Added to Bookmark"))

@app.route("/api/activity/<activity_id>/bookmark", methods=["DELETE"])
def remove_mark_act(activity_id):
    """Removes from activity from user bookmark and from database"""

    activity = Activity.query.filter_by(id=activity_id).first_or_404()
    g.user.marked_activities.remove(activity)
    db.session.commit()
    
    return jsonify(message="Deleted")
    

# Event
@app.route("/api/event/favorite", methods=["POST"])
def add_fav_event():
    """Creates Event instance and adds it to user's fav list"""
    
    id = request.json['id']

    if not Event.query.get(id):
        event = Event(
            id = request.json['id'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(event)
        db.session.commit()
    else: 
        event = Event.query.get(id) 
    
    fav_events = Favorite(
        user_id = g.user.id,
        event_id = event.id
    )
    db.session.add(fav_events)
    db.session.commit()

    return (jsonify(message="Added to Favorite"))

@app.route("/api/event/<event_id>/favorite", methods=["DELETE"])
def remove_fav_event(event_id):
    """Removes from event from user favorite and from database"""

    event = Event.query.filter_by(id=event_id).first_or_404()
    g.user.fav_events.remove(event)
    db.session.commit()

    return jsonify(message="Deleted")


@app.route("/api/event/bookmark", methods=["POST"])
def add_mark_event():
    """Creates Event instance and adds it to user's bookmark list"""

    id = request.json['id']
    
    if not Event.query.get(id):
        event = Event(
            id = request.json['id'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(event)
        db.session.commit()
    else: 
        event = Event.query.get(id) 
    
    mark_events = Bookmark(
        user_id = g.user.id,
        event_id = event.id
    )
    db.session.add(mark_events)
    db.session.commit()

    return (jsonify(message="Added to Bookmark"))

@app.route("/api/event/<event_id>/bookmark", methods=["DELETE"])
def remove_mark_event(event_id):
    """Removes from event from user bookmark and from database"""

    event = Event.query.filter_by(id=event_id).first_or_404()
    g.user.marked_events.remove(event)
    db.session.commit()
    
    return jsonify(message="Deleted")


# Place
@app.route("/api/place/favorite", methods=["POST"])
def add_fav_place():
    """Creates Place instance and adds it to user's fav list"""
    
    id = request.json['id']

    if not Place.query.get(id):
        place = Place(
            id = request.json['id'],
            image_url = request.json['imageUrl'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(place)
        db.session.commit()
    else: 
        place = Place.query.get(id) 
    
    fav_places = Favorite(
        user_id = g.user.id,
        place_id = place.id
    )
    db.session.add(fav_places)
    db.session.commit()

    return (jsonify(message="Added to Favorite"))

@app.route("/api/place/<place_id>/favorite", methods=["DELETE"])
def remove_fav_place(place_id):
    """Removes from place from user favorite and from database"""

    place = Place.query.filter_by(id=place_id).first_or_404()
    g.user.fav_places.remove(place)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route("/api/place/bookmark", methods=["POST"])
def add_mark_place():
    """Creates Place instance and adds it to user's bookmark list"""

    id = request.json['id']
    
    if not Place.query.get(id):
        place = Place(
            id = request.json['id'],
            image_url = request.json['imageUrl'],
            title = request.json['title'],
            description = request.json['description']
        )
        db.session.add(place)
        db.session.commit()
    else: 
        place = Place.query.get(id) 
    
    mark_places = Bookmark(
        user_id = g.user.id,
        place_id = place.id
    )
    db.session.add(mark_places)
    db.session.commit()

    return (jsonify(message="Added to Bookmark"))

@app.route("/api/place/<place_id>/bookmark", methods=["DELETE"])
def remove_mark_place(place_id):
    """Removes from place from user bookmark and from bookmark-database"""

    place = Place.query.filter_by(id=place_id).first_or_404()
    g.user.marked_places.remove(place)
    db.session.commit()
    
    return jsonify(message="Deleted")


# from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Setup Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

# # working below
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)
import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


from forms import UserSignUpForm, LoginForm, ChangePasswordForm
from models import db, connect_db, User

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
            )
            db.session.commit()
            

        except IntegrityError:
            import pdb
            pdb.set_trace()
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

# USER PROFILE ROUTES

@app.route('/users/<int:user_id>')
def profile(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)
    
    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_profile(user_id):
    """Show user edit form and update user data"""

    if not g.user:
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
            # import pdb
            # pdb.set_trace()
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


# ------------------HOMEPAGE------------

@app.route('/')
def logout():
    """Show homepage"""

    return render_template('homepage.hmtl')



@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_authorized(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 401
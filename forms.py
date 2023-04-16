from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo


class UserSignUpForm(FlaskForm):
    """Form for adding users."""
    
    username = StringField(
        "Username", 
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=50)],        
    )
    email = StringField(
        "Email", 
        validators=[InputRequired(), Email()],
    )
    first_name = StringField(
        'First Name', 
        validators=[InputRequired(), Length(max=30)]
    )
    last_name = StringField(
        'Last Name', 
        validators=[InputRequired(), Length(max=30)]
    )
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    remember_me = BooleanField('Remember me')

class ChangePasswordForm(FlaskForm):
    """Form for resetting password"""

    password = PasswordField('Password', validators=[Length(min=6)])
    new_password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


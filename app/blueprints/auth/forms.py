from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, FileField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

# FORMS SECTION


class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon name', validators=[DataRequired()])
    submit_btn = SubmitField('Enter')

class Login(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignUp(FlaskForm):
    # image = FileField('Profile Picture: ')
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Sign Up')

class EditProfile(FlaskForm):
    # image = FileField('Profile Picture: ')
    first_name = StringField('First Name: ')
    last_name = StringField('Last Name: ')
    submit_btn = SubmitField('Update')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField

# FORMS SECTION


class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon name')
    submit_btn = SubmitField('Enter')

class Login(FlaskForm):
    email = EmailField('Email: ')
    password = PasswordField('Password: ')
    submit_btn = SubmitField('Login')

class SignUp(FlaskForm):
    email = EmailField('Email: ')
    password = PasswordField('Password: ')
    submit_btn = SubmitField('Sign Up')
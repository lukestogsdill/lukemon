from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo

# FORMS SECTION

class Login(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignUp(FlaskForm):
    img_url = StringField('Picture Url: ')
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Sign Up')

class EditProfile(FlaskForm):
    img_url = StringField('Picture Url: ')
    first_name = StringField('First Name: ')
    last_name = StringField('Last Name: ')
    submit_btn = SubmitField('Update')

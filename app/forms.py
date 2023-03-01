from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

# FORMS SECTION
class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon name')
    submit_btn = SubmitField('Enter')
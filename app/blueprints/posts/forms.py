from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    caption = StringField('Caption', validators=[DataRequired()])
    submit_btn = SubmitField('Post')
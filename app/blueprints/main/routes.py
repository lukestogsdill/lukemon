from flask import render_template, request
from . import main
from flask_login import current_user
from ...models import PostFight, User

@main.route('/', methods=['GET'])
def home():
    posts = PostFight.query.all()
    users = User.query.all()
    return render_template('home.html', posts=posts, users=users)


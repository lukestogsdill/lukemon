from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm
from . import posts
from ...models import PostFight, User

# Create a Post
@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our form data and storing into a dict
        new_post_data = {
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Create instance of Post
        new_post = PostFight()

        # Implementing values from our form data for our instance
        new_post.from_dict(new_post_data)

        # Save user to database
        new_post.save_to_db()

        flash('You have successfully made a post!', 'success')
        return redirect(url_for('main.home'))
    return render_template('post_fight.html', form=form)
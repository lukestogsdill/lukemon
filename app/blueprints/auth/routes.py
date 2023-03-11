from flask import render_template, request, flash, redirect, url_for
from .forms import Login, SignUp, EditProfile
from . import auth
from ...models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('main.home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)
        
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'success')
        return redirect(url_for('main.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp()
    if request.method == 'POST' and form.validate_on_submit():
    # Grabbing our form data and storing into a dict
        new_user_data = {
            'img_url': form.img_url.data,
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        print(new_user_data)

        # Create instance of User
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save user to database
        new_user.save_to_db()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()
    if request.method == 'POST' and form.validate_on_submit():

        new_user_data = {
            'img_url': form.img_url.data,
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
        }
         
        #add changes to db
        current_user.update_from_dict(new_user_data)
        current_user.update_to_db()
        flash('Profile Updated!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_profile.html', form=form)
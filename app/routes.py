from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import PokeForm, Login, SignUp
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')

@app.route('/pokeform', methods=['GET', 'POST'])
def pokeform():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        poke_name = form.poke_name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        if response.ok and poke_name != None:
            poke_data = response.json()
            new_poke_data = []
            caught_pokemon = {
                'name': poke_data['name'],
                'first_move': poke_data['moves'][0]['move']['name'],
                'base_experience': poke_data['base_experience'],
                'sprite_url': poke_data['sprites']['versions']['generation-v']['black-white']['animated']['front_default'],
                'base_attack': poke_data['stats'][1]['base_stat'],
                'base_hp': poke_data['stats'][0]['base_stat'],
                'base_defense': poke_data['stats'][2]['base_stat']
            }
            new_poke_data.append(caught_pokemon)
            return render_template('pokeform.html', new_poke_data=new_poke_data, form=form)
        else:
            error = "pokemon doesn't exist"
            return render_template('pokeform.html', error=error, form=form)
    return render_template('pokeform.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully Logged In! Welcome back, {queried_user.first_name}!', 'success')            
            return redirect(url_for('home'))
        else:
            error = 'Incorrect Email/Password!'
            flash(f'{error}', 'danger')
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)
        
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'success')
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp()
    if request.method == 'POST' and form.validate_on_submit():
    # Grabbing our form data and storing into a dict
        new_user_data = {
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
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
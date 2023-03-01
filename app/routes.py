from flask import render_template, request
import requests
from app.forms import PokeForm
from app import app

@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@app.route('/pokeform', methods=['GET', 'POST'])
def pokeform():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        poke_name = form.poke_name.data
        print(poke_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        if response.ok:
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
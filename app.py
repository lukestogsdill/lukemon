from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@app.route('/pokeform', methods=['GET', 'POST'])
def pokeform():
    if request.method == 'POST':
        poke_name = request.form.get('poke_name').lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        if response.ok:
            poke_data = response.json()
            new_poke_data = []
            caught_pokemon = {
                'name': poke_data['name'],
                'first_move': poke_data['moves'][0]['move']['name'],
                'base_experience': poke_data['base_experience'],
                'sprite_url': poke_data['sprites']['front_shiny'],
                'base_attack': poke_data['stats'][1]['base_stat'],
                'base_hp': poke_data['stats'][0]['base_stat'],
                'base_defense': poke_data['stats'][2]['base_stat']
            }
            new_poke_data.append(caught_pokemon)
            return render_template('pokeform.html', new_poke_data=new_poke_data)
        else:
            error = "pokemon doesn't exist"
            return render_template('pokeform.html', error=error)
    return render_template('pokeform.html')

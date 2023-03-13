from flask import render_template, request, flash, redirect, url_for, session
import requests
from . import team
from ...models import Lukemon, User, PokeHash
from flask_login import login_required, current_user
from random import randrange, random

@team.route('/pokeroll', methods=['GET','POST'])
@login_required
def pokeroll():
    if request.method == 'POST':
        lukemon_data = generate_pokemon()
        new_stats_data = lukemon_stats(lukemon_data[0]['poke_name'])
        poke_check = PokeHash.query.filter_by(poke_name=new_stats_data[0]['poke_name']).first()
        if poke_check:
            session['poke_hash_id'] = poke_check.id
        else:
            new_poke_hash = PokeHash()
            new_poke_hash.from_dict(new_stats_data[0])
            new_poke_hash.save_to_db()
            session['poke_hash_id'] = new_poke_hash.id
        session['lukemon_data'] = lukemon_data
        return render_template('pokeroll.html', lukemon_data=lukemon_data, new_stats_data=new_stats_data)
    return render_template('pokeroll.html')


@team.route('/pokecatch', methods=['GET','POST'])
@login_required
def pokecatch():
    if request.method == 'POST':
        poke_hash_id = session.get('poke_hash_id')
        lukemon_data = session.get('lukemon_data')
        lukemon_data[0]['poke_hash_id'] = poke_hash_id        
        if len(list(current_user.teams)) < 5:
            new_lukemon = Lukemon()
            new_lukemon.from_dict(lukemon_data[0])
            new_lukemon.save_to_db()
            current_user.add_to_team(new_lukemon)
        else:
            flash(f'Your team is full', 'danger')
        return render_template('pokeroll.html')
    return render_template('pokeroll.html')

@team.route('/poketeam')
@login_required
def poketeam():
    return render_template('poketeam.html')


@team.route('/poke_del/<int:poke_id>')
@login_required
def poke_del(poke_id):
    poke = Lukemon.query.get(poke_id)
    current_user.remove_from_team(poke)
    return redirect(url_for('team.poketeam'))

def lukemon_stats(poke_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
    response = requests.get(url)
    poke_data = response.json()
    new_stats_data = []
    caught_pokemon = {
        'poke_name': poke_data['name'],
        'sprite_url': poke_data['sprites']['versions']['generation-v']['black-white']['animated']['front_default'],
        'hp': int(poke_data['stats'][0]['base_stat']*1.5),
        'att': poke_data['stats'][1]['base_stat'] + poke_data['stats'][3]['base_stat'],
        'defe': poke_data['stats'][2]['base_stat'] + poke_data['stats'][4]['base_stat'],
        'speed': poke_data['stats'][5]['base_stat']
    }
    new_stats_data.append(caught_pokemon)
    return new_stats_data

def generate_pokemon():
    lukemon_data=[]
    luke_dict = {
        'poke_name': randrange(1,649,1),
        'damage': randrange(50,150,1),
        'crit': round(random(),2),
        'accuracy': round(random(),2)
    }
    lukemon_data.append(luke_dict)
    return lukemon_data
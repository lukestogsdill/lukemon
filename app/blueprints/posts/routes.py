from flask import request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .forms import PostForm
from . import posts
from ...models import PostFight, User
from random import random
import time

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

@posts.route('/auto_battle/<int:user_id>')
@login_required
def auto_battle(user_id):
    player_team = current_user.teams
    banker_team = User.query.get(user_id)
    battle_continue = True
    player_data, banker_data, data_log = [], [], []
    
    
    for player in player_team:
        player_dict = {
            'name': player.lukemon.poke_name,
            'sprite_url': player.lukemon.sprite_url,
            'hp': player.lukemon.hp,
            'att': player.lukemon.att,
            'defe': player.lukemon.defe,
            'speed': player.lukemon.speed,
            'dmg': player.damage,
            'crit': player.crit,
            'acc': player.accuracy,
            'is_alive': True
        }
        player_data.append(player_dict)
    
    for banker in banker_team.teams:
        banker_dict = {
            'name': banker.lukemon.poke_name,
            'sprite_url': banker.lukemon.sprite_url,
            'hp': banker.lukemon.hp,
            'att': banker.lukemon.att,
            'defe': banker.lukemon.defe,
            'speed': banker.lukemon.speed,
            'dmg': banker.damage,
            'crit': banker.crit,
            'acc': banker.accuracy,
            'is_alive': True
        }
        banker_data.append(banker_dict)

    while battle_continue:
        # time.sleep(.1)
        player_load = poke_loader(player_data)
        banker_load = poke_loader(banker_data)

        if player_load == None:
            winner = 'Banker Wins!'
            battle_continue = False
        elif banker_load == None:
            winner = 'Player Wins!'
            battle_continue = False
        else:
            data_log.append(session.get('data_log'))
            battle_turn(player_load, banker_load)

        
    return render_template('auto_battle.html', banker_team=banker_team, data_log=data_log, winner=winner)  

def battle_turn(player,banker, data_log = []):
    data_log.append(f'========| {player["name"]} Hp: {player["hp"]} |========| {banker["name"]} HP: {banker["hp"]} |========')
    print(f'\n========| {player["name"]} Hp: {player["hp"]} |========| {banker["name"]} HP: {banker["hp"]} |========')

    if player['speed'] > banker['speed']:

        # player goes first
        dmg = damage_dealt(player,banker)
        banker['hp'] -= dmg

        data_log.append(f'{player["name"]} hit {banker["name"]} for {dmg} damage')
        print(f'\n{player["name"]} hit {banker["name"]} for {dmg} damage')

        if player['hp'] > 0 and banker['hp'] < 0:
            banker['is_alive'] = False
            data_log.append(f'{banker["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {banker["name"]} has fainted...')
            return(player, banker, data_log)
        elif banker['hp'] > 0 and player['hp'] < 0:
            player['is_alive'] = False
            data_log.append(f'{player["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {player["name"]} has fainted...')
            return(player, banker, data_log)
        
        dmg = damage_dealt(banker,player)
        player['hp'] -= dmg

        data_log.append(f'{banker["name"]} hit {player["name"]} for {dmg} damage')
        print(f'\n{banker["name"]} hit {player["name"]} for {dmg} damage')

        if player['hp'] > 0 and banker['hp'] < 0:
            banker['is_alive'] = False
            data_log.append(f'{banker["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {banker["name"]} has fainted...')
            return(player, banker, data_log)
        elif banker['hp'] > 0 and player['hp'] < 0:
            player['is_alive'] = False
            data_log.append(f'{player["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {player["name"]} has fainted...')
            return(player, banker, data_log)
        
    else:

        # banker goes first
        dmg = damage_dealt(banker,player)
        player['hp'] -= dmg

        data_log.append(f'{banker["name"]} hit {player["name"]} for {dmg} damage')
        print(f'\n{banker["name"]} hit {player["name"]} for {dmg} damage')

        if player['hp'] > 0 and banker['hp'] < 0:
            banker['is_alive'] = False
            data_log.append(f'{banker["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {banker["name"]} has fainted...')
            return(player, banker, data_log)
        elif banker['hp'] > 0 and player['hp'] < 0:
            player['is_alive'] = False
            data_log.append(f'{player["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {player["name"]} has fainted...')
            return(player, banker, data_log)
        
        
        dmg = damage_dealt(player,banker)
        banker['hp'] -= dmg

        data_log.append(f'{player["name"]} hit {banker["name"]} for {dmg} damage')
        print(f'\n{player["name"]} hit {banker["name"]} for {dmg} damage')
        
        if player['hp'] > 0 and banker['hp'] < 0:
            banker['is_alive'] = False
            data_log.append(f'{banker["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {banker["name"]} has fainted...')
            return(player, banker, data_log)
        elif banker['hp'] > 0 and player['hp'] < 0:
            player['is_alive'] = False
            data_log.append(f'{player["name"]} has fainted...')
            session['data_log'] = data_log
            print(f'\n {player["name"]} has fainted...')
            return(player, banker, data_log)
        
    battle_turn(player,banker)

def poke_loader(team):
    for poke in team:
        if poke['is_alive']:
             return poke
    return None

def damage_dealt(poke1, poke2):
    crit, acc = 1,1
    poke_crit_dice = random()
    poke_acc_dice = random()
    if poke_crit_dice <= poke1['acc']:
        acc = 0
        print(f'\n{poke1["name"]} attacks {poke2["name"]} and misses')
    if poke_acc_dice <= poke1['crit']:
        crit = 1.5
        print(f'{poke1["name"]} attacks {poke1["name"]} and crits')

    return (poke1['dmg']*(poke1['att']/poke2['defe'])/2)*crit*acc
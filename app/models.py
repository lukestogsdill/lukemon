from app import db,login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


team=db.Table('team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('lukemon_id', db.Integer, db.ForeignKey('lukemon.id'))
    )
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    post_fight = db.relationship('PostFight', backref='author', lazy='dynamic')
    teams = db.relationship('Lukemon', secondary=team, backref='teams', lazy='dynamic') 

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    # check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # use this method to register our user attributes
    def from_dict(self, data):
        self.img_url = data['img_url']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    def update_from_dict(self, data):
        self.img_url = data['img_url']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()
    
    def add_to_team(self, lukemon):
        self.teams.append(lukemon)
        db.session.commit()
    
    def remove_from_team(self, lukemon):
        self.teams.remove(lukemon)
        db.session.commit()

class PokeHash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String, nullable=False)
    sprite_url = db.Column(db.String, nullable=False)
    hp = db.Column(db.Integer, nullable=False)
    att = db.Column(db.Integer, nullable=False)
    defe = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    lukemon = db.relationship('Lukemon', backref='lukemon', lazy='dynamic')
    
    def from_dict(self, data):
        self.poke_name = data['poke_name']
        self.sprite_url = data['sprite_url']
        self.hp = data['hp']
        self.att = data['att'] 
        self.defe = data['defe'] 
        self.speed = data['speed']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
class Lukemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    damage = db.Column(db.Integer, nullable=False)
    crit = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    poke_hash_id = db.Column(db.Integer, db.ForeignKey('poke_hash.id'))

    def from_dict(self, data):
        self.damage = data['damage']
        self.crit = data['crit']
        self.accuracy = data['accuracy']
        self.poke_hash_id = data['poke_hash_id']
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()




class PostFight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    # Foreign Key to user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def from_dict(self, data):
        self.caption = data['caption']
        self.user_id = data['user_id']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_post(self):
        db.session.delete(self)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
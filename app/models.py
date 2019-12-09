from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

playersAtGame = db.Table('playersAtGame',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
        )

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phoneNo = db.Column(db.String(16), nullable=False, unique=False)
    nokName = db.Column(db.String(50), nullable=False)
    nokNumber = db.Column(db.String(16), nullable=False, unique=False)
    games = db.relationship('Game', secondary=playersAtGame, backref=db.backref('players'), lazy=True)

    def __repr__(self):
        return "User {},{}".format(self.name, self.email)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=True)
    opposition = db.Column(db.String(30), nullable=False)
    result = db.Column(db.String(35), nullable=True)

def __repr__(self):
        return "The game agaist {} is on {}".format(self.opposition, self.date)

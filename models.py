import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    __password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    birthday = db.Column(db.Date)
    height = db.Column(db.Integer)
    weights = db.relationship('Weight', back_populates='user', order_by='desc(Weight.date)')
    steps = db.relationship('Steps', back_populates='user')

    def __init__(self, email):
        self.email = email

    # https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
    def set_password(self, password):
        self.__password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def current_weight(self):
        return self.weights[0] if self.weights else 0

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='weights')

    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    weight = db.Column(db.Numeric(scale=2))

    def __init__(self, weight):
        self.weight = weight

# TODO: Log ingredients and exercise

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='steps')
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    steps = db.Column(db.Integer)

    def __init__(self, steps):
        self.steps = steps


class Ingredient(db.Model):
    __tablename__ = 'Ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    kcal_per_100_gram = db.Column(db.Integer)


class Exercise(db.Model):
    __tablename__ = 'Exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    kcal_per_rep = db.Column(db.Integer)

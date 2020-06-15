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
    points = db.Column(db.Integer)

    def __init__(self, email):
        self.email = email

    # https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem
    def set_password(self, password):
        self.__password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)

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

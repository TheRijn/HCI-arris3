#! /usr/bin/env python3
from flask import Flask

from models import db, User, Steps
from datetime import date, datetime
from csv import DictReader

app = Flask(__name__)
db.init_app(app)

def create_user():
    user = User(email="user@example.com")
    user.set_password("1234")
    user.first_name = "John"
    user.last_name = "Appleseed"
    user.birthday = date(1990, 1, 1)
    user.height = 180
    db.session.add(user)
    db.session.commit()
    return user

if __name__ == '__main__':
    user = create_user()
    with open("data/steps.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            steps = Steps(steps=line['steps'])
            steps.date = datetime.fromisoformat(line['datetime'])
            db.session.add(steps)
        db.session.commit()

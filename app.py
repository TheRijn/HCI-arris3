from csv import DictReader
from datetime import datetime, date
from pathlib import Path
import sys

import click
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_migrate import Migrate, upgrade

from forms import LoginForm, RegistrationForm, ProfileForm, AddWeightForm, LogExerciseForm, LogFoodForm, AddStepsForm
from models import db, User, Weight, Ingredient, Exercise, Steps, ExerciseLog, FoodLog

app = Flask(__name__)

app.config['SECRET_KEY'] = "this-is-really-secret"

# Setup db and migrations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flask-admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Weight, db.session))
admin.add_view(ModelView(Steps, db.session))
admin.add_view(ModelView(Ingredient, db.session))
admin.add_view(ModelView(Exercise, db.session))
admin.add_view(ModelView(FoodLog, db.session))
admin.add_view(ModelView(ExerciseLog, db.session))

# Flask Bootstrap
Bootstrap(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_filter('formatdate')
def format_date(value, format="%d %B %Y"):
    """Format a date time to (Default): d Mon YYYY"""
    if value is None:
        return ""
    return value.strftime(format)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print(request.form)

    user: User = current_user

    weights = user.weights_dict()
    steps = user.steps_dict()
    today = datetime.today()
    points = []
    message = "You can still log your current weight and steps to gain points, make over 10000 steps to make even more points."
    for weight in weights:
        if (today.strftime("%m/%d/%y") in weight.values()):
            points.append(40)
            message = "Try to make more then 10000 steps tommorow to gain the last 20 points."
            break

    for step in steps:
        if (today.strftime("%m/%d/%y") in step.values()):
            points.append(40)
            message = "Try to make more then 10000 steps tommorow to gain the last 20 points."
            if (step['series'] > 10000):
                points.append(20)
                message = "You've done everything for today. A full one hundred points, be proud!!"
            break

    le_form = LogExerciseForm(prefix='exercise')
    le_form.exercise.choices = [(e.id, e.name) for e in Exercise.query.all()]

    lf_form = LogFoodForm(prefix='food')
    lf_form.ingredient.choices = [(i.id, i.name) for i in Ingredient.query.all()]

    w_form = AddWeightForm(prefix='weight')

    s_form = AddStepsForm(prefix='steps')

    if lf_form.ingredient.data and lf_form.validate_on_submit():
        food_log = FoodLog(grams=lf_form.grams.data)
        food_log.user = current_user
        food_log.ingredient_id = lf_form.ingredient.data

        db.session.add(food_log)
        db.session.commit()

        flash('Food added!')
        return redirect(url_for('home'))

    if le_form.exercise.data and le_form.validate_on_submit():
        exercise_log = ExerciseLog(amount=le_form.reps.data)
        exercise_log.user = current_user
        exercise_log.exercise_id = le_form.exercise.data

        db.session.add(exercise_log)
        db.session.commit()

        flash('Exercise added!')
        return redirect(url_for('home'))

    if w_form.weight.data and w_form.validate_on_submit():
        weight = Weight(w_form.weight.data)
        weight.user = current_user
        db.session.add(weight)
        db.session.commit()

        flash('Weight added!')
        return redirect(url_for('home'))

    if s_form.steps.data and s_form.validate_on_submit():
        steps = Steps(s_form.steps.data)
        steps.user = current_user
        db.session.add(steps)
        db.session.commit()

        flash('Steps added!')
        return redirect(url_for('home'))

    return render_template('home.html', e_form=le_form, f_form=lf_form, s_form=s_form, w_form=w_form, weights=weights,
                           steps=steps, points=points, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/edit', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        user: User = current_user

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.birthday = form.birthday.data
        user.height = form.height.data

        db.session.add(user)
        db.session.commit()

        flash('Profile updated!')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)


@app.cli.command('import')
def import_data():
    if Path('db/app.db').exists():
        click.confirm('app.db already exist, want to remove it?', abort=True)
        Path('db/app.db').unlink()

    upgrade()
    user = create_user()

    with open("data/steps.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            steps = Steps(steps=line['steps'])
            steps.date = datetime.fromisoformat(line['datetime'])
            steps.user = user
            db.session.add(steps)
        db.session.commit()

    with open("data/weights.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            weight = Weight(weight=line['weight'])
            weight.date = datetime.fromisoformat(line['datetime'])
            weight.user = user
            db.session.add(weight)
        db.session.commit()

    with open("data/exercises.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            exercise = Exercise(name=line['name'], kcal_per_rep=line['kcal'])
            db.session.add(exercise)
        db.session.commit()

    with open("data/ingredients.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            ingredient = Ingredient(name=line['name'], kcal_per_100_gram=line['kcal'])
            db.session.add(ingredient)
        db.session.commit()

    with open("data/food_log.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            food_log = FoodLog()
            food_log.user = user
            food_log.ingredient_id = line['ingredient_id']
            food_log.grams = line['grams']
            food_log.timestamp = datetime.fromisoformat(line['datetime'])
            db.session.add(food_log)
        db.session.commit()

    with open("data/exercise_log.csv", 'r') as f:
        reader = DictReader(f)
        for line in reader:
            exercise_log = ExerciseLog()
            exercise_log.user = user
            exercise_log.exercise_id = line['exercise_id']
            exercise_log.amount = line['amount']
            food_log.timestamp = datetime.fromisoformat(line['datetime'])
            db.session.add(exercise_log)
        db.session.commit()


def create_user():
    user = User(email="user@example.com")
    user.set_password("1234")
    user.first_name = "John"
    user.last_name = "Appleseed"
    user.birthday = date(1990, 1, 1)
    user.height = 180
    db.session.add(user)
    db.session.commit()
    print("Created user with email: user@example.com and pasword: 1234")
    return user


if __name__ == "__main__":
    app.run()

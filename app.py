from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_migrate import Migrate

from forms import LoginForm, RegistrationForm, ProfileForm, AddWeightForm, LogExerciseForm, LogFoodForm
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
    user: User = current_user

    weights = user.weights_dict()
    steps = user.steps_dict()

    le_form = LogExerciseForm(prefix='exercise')
    le_form.exercise.choices = [(e.id, e.name) for e in Exercise.query.all()]

    lf_form = LogFoodForm(prefix='food')
    lf_form.ingredient.choices = [(i.id, i.name) for i in Ingredient.query.all()]

    if lf_form.submit.data and lf_form.validate_on_submit():
        food_log = FoodLog(grams=lf_form.grams.data)
        food_log.user = current_user
        food_log.ingredient_id = lf_form.ingredient.data

        db.session.add(food_log)
        db.session.commit()

        flash('Food added!')
        return redirect(url_for('home'))

    if le_form.submit.data and le_form.validate_on_submit():
        exercise_log = ExerciseLog(amount=le_form.reps.data)
        exercise_log.user = current_user
        exercise_log.exercise_id = le_form.exercise.data

        db.session.add(exercise_log)
        db.session.commit()

        flash('Exercise added!')
        return redirect(url_for('home'))

    return render_template('home.html', e_form=le_form, f_form=lf_form, weights=weights, steps=steps)


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


@app.route('/profile/add-weight', methods=['GET', 'POST'])
@login_required
def add_weight():
    form = AddWeightForm()

    if form.validate_on_submit():
        weight = Weight(form.weight.data)
        weight.user = current_user

        db.session.add(weight)
        db.session.commit()

        flash("Weight added")
        return redirect(url_for('profile'))

    return render_template('add_weight.html', form=form)

@app.route('/profile/log-exercise', methods=['POST'])
@login_required
def log_exercise():
    form = LogExerciseForm()
    print(request.form)
    if form.validate_on_submit():
        print(form)

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()

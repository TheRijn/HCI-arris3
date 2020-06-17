from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange

from models import User


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    birthday = DateField('Birthday (year-month-day)', render_kw={'placeholder': "1999-10-26"})
    height = IntegerField('Height (in cm)', validators=[NumberRange(100, 250, 'Please enter your height in cm.')], render_kw={'placeholder': '180'})

    submit = SubmitField('Update')


class AddWeightForm(FlaskForm):
    weight = FloatField("Weight", validators=[NumberRange(0, 300, 'Please enter your weight in kg.')], )

    submit = SubmitField('Submit')

class LogExerciseForm(FlaskForm):
    exercise = SelectField('Exercise', coerce=int)
    reps = IntegerField('Reps')

    submit = SubmitField('Add')

class LogFoodForm(FlaskForm):
    ingredient = SelectField('Ingredient', coerce=int)
    grams = IntegerField('Weight (g)')

    submit = SubmitField('Add')

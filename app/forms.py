from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateListForm(FlaskForm):
    name = StringField('My Name')
    activityDescription = StringField('Activity Description')
    activityTitle = StringField('Activity Title')
    activityType = StringField('Activity Type')
    submitListItem = SubmitField('Submit')

class HomeForm(FlaskForm):
    toCreateList = SubmitField('Create List')
    toViewList = SubmitField('View List')
    toViewCalender = SubmitField('View Calender')
    toForum = SubmitField('View Forum')
    toForumNew = SubmitField('New Forum Post')

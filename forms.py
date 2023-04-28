from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email
from wtforms.widgets import PasswordInput


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[
                             InputRequired()], widget=PasswordInput())
    email = StringField("email", validators=[InputRequired(), Email()])
    first_name = StringField("first_name", validators=[InputRequired()])
    last_name = StringField("last_name", validators=[InputRequired()])


# ! The User form will be for logging in JUST USERNAME & PASSWORD and the register form will be to register the user, when registering sometimes you have additional variables you want to save to the db. when logging in the form may just take the username and password to validate the user


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired()], widget=PasswordInput())


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[
        InputRequired()])

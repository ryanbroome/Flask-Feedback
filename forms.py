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


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired()], widget=PasswordInput())


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[
        InputRequired()])

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("sign up")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit = SubmitField("Login")
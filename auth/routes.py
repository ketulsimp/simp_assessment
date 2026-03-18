from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email

class Register(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired(),Email()])
    password=PasswordField("password")

auth=Blueprint("auth",__name__)




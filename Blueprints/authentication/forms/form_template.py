from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    email = EmailField('email',validators=[InputRequired()])
    password = PasswordField('password',validators=[InputRequired()])
    submit = SubmitField('login')

class RegisterForm(FlaskForm):
    name = StringField('name',validators=[InputRequired()])
    email = EmailField('email',validators=[InputRequired()])
    password = PasswordField('password',validators=[InputRequired()])
    submit = SubmitField('register')
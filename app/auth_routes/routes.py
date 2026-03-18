from flask import Flask,request,session,redirect,url_for,render_template,Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash,check_password_hash
from ..extensions import mongo
from app import app

@app.route('/')
def welcome():
    return redirect(url_for('register'))

class Register(FlaskForm):
    name=StringField('name',validators=[(InputRequired)])
    email=EmailField('email',validators=[(InputRequired)])
    password=PasswordField('password',validators=[(InputRequired)])


@app.route('/register',methods=['POST','GET'])
def register():
    form=Register()
    if form.validate_on_submit:
        username=request.form.data
        email=request.form.data
        password=request.form.data
        if mongo.db.users.find_one({'email':email}):
            print('---user already exist')
            return redirect(url_for('login'))
        pwd=generate_password_hash(password)
        mongo.db.users.insert_one({'name':username,'email':email,'password':pwd})
        return redirect(url_for('login'))
    render_template('register.html',form=form)

class Login(FlaskForm):
    email=EmailField('email',validators=[(InputRequired)])
    password=PasswordField('password',validators=[(InputRequired)])
@app.route('/login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validate_on_submit():
        email=request.form.data
        password=request.form.data
        query=mongo.db.users.find_one({'email':email})
        if query and check_password_hash(query.password,password):
            return redirect(url_for('dashboard'))
        return redirect(url_for('register'))
    return render_template('login.html',form=form)


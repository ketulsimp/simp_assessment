from flask import Blueprint,render_template,request, redirect, url_for, session, flash
from Blueprints.authentication.forms.form_template import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from models.mongoModel import connection, users

auth_rt = Blueprint(
    'auth_rt',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/auth'
)


@auth_rt.route('/register',methods=["GET","POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        users.insert_one({'name':name, 'email':email, 'password': hashed_password})
        return redirect(url_for('auth_rt.login')), 201
    return render_template('register.html',form=register_form), 200


@auth_rt.route('/login',methods=["GET","POST"])
def login():
    login_form=  LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user_obj =  users.find_one({'email':email})
        if user_obj is not None and check_password_hash(user_obj.get('password',''),password):
            pass
        flash('Invalid Credentials.')
        return redirect(request.base_url), 401
    return render_template('login.html', form = login_form)
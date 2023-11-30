from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError

from controller.user import UserController, SignupForm, LoginForm


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    # get form data
    email = form.email.data
    password = form.password.data
    remember = form.remember.data

    return UserController.login_user(email, password, remember)
    

@auth.route('/signup')
def signup():
    form = SignupForm(request.form)
    return render_template('signup.html', form=form)

# this method handles signup request from forms and stuff
@auth.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm(request.form)

    if not form.validate():
        return render_template('signup.html', form=form)

    # get form data
    email = form.email.data
    name = form.name.data
    password = form.password.data
    confirmed_password = form.confirmed_password.data

    return UserController.signup_user(email, name, password, confirmed_password)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError

from controller.user import UserController

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # get form data
    email = request.form.get('email')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    return UserController.login_user(email, password, remember)
    

@auth.route('/signup')
def signup():
    return render_template('signup.html')

# this method handles signup request from forms and stuff
@auth.route('/signup', methods=['POST'])
def signup_post():
    # get form data
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirmed_password = request.form.get('confirmed_password')

    return UserController.signup_user(email, name, password, confirmed_password)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

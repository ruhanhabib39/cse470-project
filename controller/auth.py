from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError


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
    

    # validating and normalizing email
    try:
        # we should set check_deliverability=True if we use email confirmation
        emailinfo = validate_email(email, check_deliverability=False) 

        email = emailinfo.normalized
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for('auth.login'))

    # retrieve user from database by their email
    # user = User.query.filter_by(email=email).first()
    user = db.session.execute(db.select(User).filter_by(email=email)).first()
    if user:
        user = user[0]

    # check if user actually exists and whether their password is correct
    if not user or not check_password_hash(user.password, password):
        flash('Wrong email or password')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

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

    # validating and normalizing email
    try:
        # we should set check_deliverability=True if we use email confirmation
        emailinfo = validate_email(email, check_deliverability=False) 

        email = emailinfo.normalized
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for('auth.signup'))

    # validate name and password
    if len(name) < 1:
        flash('Name must have at least one character')
        return redirect(url_for('auth.signup'))
    elif len(name) > NAME_MAX_LENGTH:
        flash(f'Name can not have more than {NAME_MAX_LENGTH} characters')
        return redirect(url_for('auth.signup'))
    elif len(password) < 6:
        flash('Pasword must have at least 6 characters')
        return redirect(url_for('auth.signup'))
    elif len(password) > PASSWORD_MAX_LENGTH:
        flash(f'Password can not have more thatn {PASSWORD_MAX_LENGTH} characters')
        return redirect(url_for('auth.signup'))
    elif password != confirmed_password:
        flash('Password and confirmation password did not match')
        return redirect(url_for('auth.signup'))


    # we see if a user with email already exists
    # user will None if user doesn't exist
    # otherwise, we already have a user with this email
    # user = User.query.filter_by(email=email).first()
    user = db.session.execute(db.select(User).filter_by(email=email)).first()
    if user:
        user = user[0]

    if user:
        # if user with given email already exists redirect back to the signup page and tell them
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    # if email hasn't been used previously, we can create a new user
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # and save them to the database
    db.session.add(new_user)
    db.session.commit()

    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

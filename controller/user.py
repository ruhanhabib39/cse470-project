from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError

from typing import Optional

from wtforms import Form, BooleanField, StringField, PasswordField, validators

class SignupForm(Form):
    email = StringField('Email Address', [validators.Length(min=1, max=EMAIL_MAX_LENGTH), validators.Email()])
    name = StringField('Name', [validators.Length(min=1, max=NAME_MAX_LENGTH)])
    password = PasswordField('Password', [
        validators.DataRequired(), 
        validators.EqualTo('confirmed_password', message='Passwords must match'),
        validators.Length(min=6, max=PASSWORD_MAX_LENGTH)
    ])
    confirmed_password = PasswordField('Confirm Password')

class UserController:
    # queries the database for the user, filtered by the keywords arguments
    # returns None if it doesn't exist
    # otherwise, returns first row from queryj
    # for example, UserController.get_first_user(email='test@test.com') should
    # give us the user with email = 'test@test.com'
    @staticmethod
    def get_first_user(**kwargs) -> Optional[User]:
        user = db.session.execute(db.select(User).filter_by(**kwargs)).first()
        if user:
            user = user[0]
        return user

    # this method validates and normalizes the given email
    # if the email is not valid, it flashes the mistake and returns None
    # otherwise, returns the normalized email
    @staticmethod
    def validate_and_normalize_email(email: str) -> (Optional[str], Optional[str]):
        try:
            email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError as e:
            return (None, str(e))
        return (email, None)

    # try to login the user
    @staticmethod
    def login_user(email: str, password: str, remember: bool) -> Response:
        email, error_message = UserController.validate_and_normalize_email(email)
        if error_message:
            flash(error_message)
            return redirect(url_for('auth.login'))

        user = UserController.get_first_user(email=email)

        if not user or not check_password_hash(user.password, password):
            flash('Wrong email or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))


    # validate signup data
    # returns a string describing the error if the data is invalid
    # otherwise, returns None
    @staticmethod
    def validate_signup(email: str, name: str, password: str, confirmed_password: str) -> Optional[str]:

        email, error_message = UserController.validate_and_normalize_email(email)
        if error_message: return error_message

        if UserController.get_first_user(email=email):
            flash('Email address already in use')
            return redirect(url_for('auth.signup'))

        return None

    # signup the user
    @staticmethod
    def signup_user(email: str, name: str, password: str, confirmed_password: str) -> Response:
        error_description = UserController.validate_signup(email, name, password, confirmed_password)
        if error_description:
            flash(error_description)
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

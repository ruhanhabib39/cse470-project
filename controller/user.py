from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError

from typing import Optional

class UserController:
    # queries the database for the user, filtered by the keywords arguments
    # returns None if it doesn't exist
    # otherwise, returns first row from queryj
    # for example, UserController.get_first_user(email='test@test.com') should
    # give us the user with email = 'test@test.com'
    @classmethod
    def get_first_user(cls, **kwargs) -> Optional[User]:
        user = db.session.execute(db.select(User).filter_by(**kwargs)).first()
        if user:
            user = user[0]
        return user

    # this method validates and normalizes the given email
    # if the email is not valid, it flashes the mistake and returns None
    # otherwise, returns the normalized email
    @classmethod
    def validate_and_normalize_email(cls, email: str) -> (Optional[str], Optional[str]):
        try:
            email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError as e:
            return (None, str(e))
        return (email, None)

    # try to login the user
    @classmethod
    def login_user(cls, email: str, password: str, remember: bool) -> Response:
        email, error_message = cls.validate_and_normalize_email(email)
        if error_message:
            flash(error_message)
            return redirect(url_for('auth.login'))

        user = cls.get_first_user(email=email)

        if not user or not check_password_hash(user.password, password):
            flash('Wrong email or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))


    # validate signup data
    # returns a string describing the error if the data is invalid
    # otherwise, returns None
    @classmethod
    def validate_signup(cls, email: str, name: str, password: str, confirmed_password: str) -> Optional[str]:

        email, error_message = cls.validate_and_normalize_email(email)
        if error_message: return error_message

        # validate name and password
        if len(name) < 1:
            return 'Name must have at least one character'
        elif len(name) > NAME_MAX_LENGTH:
            return f'Name can not have more than {NAME_MAX_LENGTH} characters'
        elif len(password) < 6:
            return 'Pasword must have at least 6 characters'
        elif len(password) > PASSWORD_MAX_LENGTH:
            return f'Password can not have more thatn {PASSWORD_MAX_LENGTH} characters'
        elif password != confirmed_password:
            return 'Password and confirmation password did not match'

        if cls.get_first_user(email=email):
            flash('Email address already in use')
            return redirect(url_for('auth.signup'))

        return None

    # signup the user
    @classmethod
    def signup_user(cls, email: str, name: str, password: str, confirmed_password: str) -> Response:
        error_description = cls.validate_signup(email, name, password, confirmed_password)
        if error_description:
            flash(error_description)
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

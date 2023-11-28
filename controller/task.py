
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from model.task import Task, TASK_TITLE_MAX_LENGTH, TASK_DESC_MAX_LENGTH
from model.task import Category, Tag
from project import db

from email_validator import validate_email, EmailNotValidError

import typing

import re

from abc import ABC, abstractmethod

class TagAndCategoryController(ABC):
    @classmethod
    @abstractmethod
    def get_model(cls):
        assert False

    @classmethod
    @abstractmethod
    def get_front_letter(cls) -> str:
        assert False

    @classmethod
    @abstractmethod
    def parse(cls, desc: str) -> typing.List[str]:
        pattern = cls.get_front_letter() + r'(\w+)'
        return [m[1] for m in re.finditer(pattern, desc)]

    # get by name, if it exists
    # if it doesn't exist, returns None
    @classmethod
    @abstractmethod
    def get(cls, name: str):
        res = db.session.execute(db.select(cls.get_model()).filter_by(name=name)).first()
        if res:
            res = res[0]
        return res

    # get by name, if it exists
    # otherwise, create it, add it the database, and return
    @classmethod
    @abstractmethod
    def get_plus_create(cls, name: str):
        stuff = cls.get(name)
        if not stuff:
            model = cls.get_model()
            stuff = model(name=name)
            db.session.add(stuff)
            db.session.commit()
        return stuff

class TagController(TagAndCategoryController):
    @classmethod
    def get_model(cls):
        return Tag

    @classmethod
    def get_front_letter(cls) -> str:
        return '#'

class CategoryController(TagAndCategoryController):
    @classmethod
    def get_model(cls):
        return Category

    @classmethod
    def get_front_letter(cls) -> str:
        return '@'

class TaskController:
    # TODO
    pass

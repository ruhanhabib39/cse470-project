
from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_login import login_user, login_required, logout_user, current_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from model.task import Task, TASK_TITLE_MAX_LENGTH, TASK_DESC_MAX_LENGTH
from model.task import Category, Tag
from project import db

from email_validator import validate_email, EmailNotValidError

import typing

import re

from abc import ABC, abstractmethod

import datetime

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

    @classmethod
    @abstractmethod
    def get_plus_create_all(cls, desc: str):
        return list(set((cls.get_plus_create(word) for word in cls.parse(desc))))

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
    @staticmethod
    def create_task(title: str, desc: str, priority: int, due_date: datetime.date,
            user_id: int, user: User) -> Response:
        task = Task(title=title, desc=desc, priority=priority, due_date=due_date,
                user_id=user_id, user=user)
        task.tags = TagController.get_plus_create_all(desc)
        task.categories = CategoryController.get_plus_create_all(desc)

        db.session.add(task)
        db.session.commit()

        return redirect(url_for('main.tasks'))

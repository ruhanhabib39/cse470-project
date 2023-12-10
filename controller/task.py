
from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_login import login_user, login_required, logout_user, current_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from model.task import Task, TASK_TITLE_MAX_LENGTH, TASK_DESC_MAX_LENGTH
from model.task import Category, Tag, Attachment
from project import db, ATTACHMENT_FOLDER
from datetime import datetime
from flask import jsonify

from email_validator import validate_email, EmailNotValidError

from werkzeug.utils import secure_filename

import typing

import re

from abc import ABC, abstractmethod

import datetime

from wtforms import Form, validators
from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.fields import DateTimeLocalField, SelectField

from flask_wtf import FlaskForm
from flask_wtf.file import FileField

import os

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
        return set((cls.get_plus_create(word) for word in cls.parse(desc)))

    @classmethod
    @abstractmethod
    def get_plus_create_from_semicolon_string(cls, desc: str):
        tokens = map(str.strip, desc.strip().split(';'))
        nonempty_tokens = filter(lambda tok: len(tok) != 0, tokens)
        old_style_desc = ' '.join([cls.get_front_letter() + token for token in nonempty_tokens])
        return cls.get_plus_create_all(old_style_desc)



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

class TaskForm(FlaskForm):
    title = StringField('Title',
            [validators.Length(min=1, max=TASK_TITLE_MAX_LENGTH)])
    due_date = DateTimeLocalField('Due Date')
    priority = SelectField('Priority', 
            choices=[('1','Very High'),
                     ('2','High'),
                     ('3','Medium'),
                     ('4', 'Low'),
                     ('5', 'Very Low')])
    desc = TextAreaField('Description',
            [validators.Length(min=1, max=TASK_DESC_MAX_LENGTH)])
    tags = StringField('Tags')
    categories = StringField('Categories')
    subtasks = SelectField('Add Subtask', coerce=int)
    files = FileField('Upload File') 

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

    @staticmethod
    def get_tasks(**kwargs) -> typing.List[Task]:
        return db.session.scalars(db.select(Task).filter_by(**kwargs)).all()

    @staticmethod
    def get_first_task(**kwargs) -> Task | None:
        return db.session.scalar(db.select(Task).filter_by(**kwargs))

    # gets the root task of the tree containing the given task
    @staticmethod
    def get_root(task: Task) -> Task:
        root = task
        while root.parent_id:
            root = TaskController.get_first_task(id=root.parent_id)
        return root


    @staticmethod
    def update_task(form: TaskForm, tsk: Task):
        task_id = tsk.id

        tsk.title = form.title.data
        tsk.due_date = form.due_date.data
        tsk.priority = form.priority.data
        tsk.desc = form.desc.data
        tsk.tags = TagController.get_plus_create_from_semicolon_string(form.tags.data)
        tsk.categories = CategoryController.get_plus_create_from_semicolon_string(form.categories.data)

        db.session.commit()

        if (subtask := TaskController.get_first_task(id=form.subtasks.data)) and (not subtask.parent_id):
            tsk.children.append(subtask)
            db.session.commit()

        if form.files.data and form.files.data.filename:

            filename = secure_filename(form.files.data.filename)
            
            attachment = Attachment(name=filename, task_id=task_id, task=tsk)

            if not os.path.exists(ATTACHMENT_FOLDER):
                os.makedirs(ATTACHMENT_FOLDER)


            file = request.files['files']


            db.session.add(attachment)
            db.session.commit()

            db.session.refresh(attachment)

            file.save(os.path.join(ATTACHMENT_FOLDER, str(attachment.id)))

    @staticmethod
    def mark_complete(task: Task):
        if not task.completed:
            task.completion_date = datetime.datetime.today()

        task.completed = True
        db.session.commit()

        for child in task.children:
            TaskController.mark_complete(child)

    @staticmethod
    def archive(task: Task, value: bool):
        task.archived = value
        db.session.commit()

        for child in task.children:
            TaskController.archive(child, value)

    @staticmethod
    def delete(task: Task):
        db.session.delete(task)
        db.session.commit()

    def restore(self, task: Task):
        task.restored = True
        task.archived = False
        db.session.commit()
    



#
#def complete_task(task_id):
#    task = Task.query.get(task_id)
#    task.completed = True
#    task.completion_date = datetime.now()
#    db.session.commit()
#    return redirect(url_for('main.tasks'))

task = Blueprint('task', __name__)

@task.route('/task_history')
@login_required
def task_history():
    tasks = Task.query.filter_by(completed=True, user_id=current_user.id).order_by(Task.completion_date.desc()).all()
    return render_template('task_history.html', tasks=tasks)

@task.route('/export_data', methods=['GET'])
@login_required
def export_data():
    tasks = TaskController.get_tasks(user_id=current_user.id)
    task_dicts = [task.to_dict() for task in tasks]
    return jsonify(task_dicts)
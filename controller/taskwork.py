from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from model.user import User, EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH, NAME_MAX_LENGTH
from model.task import Task, TASK_TITLE_MAX_LENGTH, TASK_DESC_MAX_LENGTH
from project import db

from email_validator import validate_email, EmailNotValidError

from controller.task import TaskController, TagController, CategoryController


taskwork = Blueprint('taskwork', __name__)

@taskwork.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    desc = request.form.get('desc')
    priority = 1

    import datetime

    due_date = datetime.date.today() + datetime.timedelta(days=1)

    if len(title) > TASK_TITLE_MAX_LENGTH:
        flash('Title too long')
        return redirect(url_for('main.tasks'))
    elif len(desc) > TASK_DESC_MAX_LENGTH:
        flash('Description too long')
        return redirect(url_for('main.tasks'))

    return TaskController.create_task(title, desc, priority, due_date, current_user.id, current_user)


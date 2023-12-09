from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask import flash, jsonify, send_file
from flask_login import login_required, current_user
from project import db, ATTACHMENT_FOLDER

from werkzeug.utils import secure_filename

from controller.task import TaskForm, TaskController, TagController, CategoryController

from model.task import Attachment

import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/tasks')
@login_required
def tasks():
    task_ids = [t.id for t in current_user.tasks]
    return render_template('tasks.html', task_ids=task_ids, task_list=current_user.tasks)

@main.route('/task/<int:task_id>', methods=["GET", "POST"])
@login_required
def task(task_id):
    tsk_list = TaskController.get_tasks(id=task_id)
    if not tsk_list or tsk_list[0].user_id != current_user.id:
        flash('Task not available')
        return redirect(url_for('main.tasks'))

    tsk = tsk_list[0]

    tree_root = TaskController.get_root(tsk)

    is_good = lambda x: x.id != tree_root.id and (not x.parent_id)
    good_tasks = filter(is_good, current_user.tasks)
    subtask_choices = [(0, "")] + [(t.id, t.title) for t in good_tasks]

    form = TaskForm()
    form.subtasks.choices = subtask_choices

    if request.method == 'POST':
        if not form.validate():
            return render_template('task.html', task=tsk, task_id=task_id, form=form)

        TaskController.update_task(form, tsk)
    else:
        form.process(obj=tsk)

        form.tags.data = '; '.join([x.name for x in tsk.tags])
        form.categories.data = '; '.join([x.name for x in tsk.categories])

    return render_template('task.html', task=tsk, task_id=task_id, form=form)


@main.route('/attachments/<int:attachment_id>')
@login_required
def attachments(attachment_id):
    attachment = db.session.scalar(db.select(Attachment).filter_by(id=attachment_id))
    if not attachment or attachment.task.user_id != current_user.id:
        abort(403)

    file_dir = os.path.join(ATTACHMENT_FOLDER, str(attachment.id))
    return send_file(file_dir, download_name=attachment.name)

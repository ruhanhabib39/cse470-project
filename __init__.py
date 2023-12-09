from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
# adds the current directory to path
sys.path.append(current_dir)

# setting up the database
db = SQLAlchemy()

csrf = CSRFProtect()

ATTACHMENT_FOLDER = ''

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py') # reading config stuff from config.py

    global ATTACHMENT_FOLDER
    ATTACHMENT_FOLDER = app.config['ATTACHMENT_FOLDER']

    db.init_app(app)
    csrf.init_app(app)

    # be careful about the order of import
    # the following can not be imported twice
    from model.user import User
    from model.task import Task, Category, Tag

    from controller.auth import auth as auth_blueprint
    from controller.main import main as main_blueprint
    from controller.taskwork import taskwork as task_blueprint
    from controller.user import user as user_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(user_blueprint)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app



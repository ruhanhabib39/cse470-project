from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
# adds the current directory to path
sys.path.append(current_dir)

# setting up the database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py') # reading config stuff from config.py

    db.init_app(app)

    # be careful about the order of import
    # the following can not be imported twice
    from model.user import User
    from model.task import Task, Category, Tag

    from controller.auth import auth as auth_blueprint
    from controller.main import main as main_blueprint
    from controller.taskwork import taskwork as task_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(task_blueprint)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app



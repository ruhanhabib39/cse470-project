import os

current_dir = os.path.dirname(os.path.realpath(__file__))

ENV = 'development'
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))

# SQLALCHEMY_DATABASE_URI = f'sqlite:///{current_dir}/db.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(current_dir, 'db.sqlite')

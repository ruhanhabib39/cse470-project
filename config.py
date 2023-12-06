import os

current_dir = os.path.dirname(os.path.realpath(__file__))

ENV = 'development'
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))

ATTACHMENT_FOLDER = os.path.join(current_dir, 'attachments')

MAX_CONTENT_LENGTH = 32 * 1000 * 1000

# SQLALCHEMY_DATABASE_URI = f'sqlite:///{current_dir}/db.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(current_dir, 'db.sqlite')

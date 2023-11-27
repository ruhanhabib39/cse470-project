
import os
current_dir = os.path.dirname(os.path.realpath(__file__))

SECRET_KEY = None
with open(f'{current_dir}/secret.txt', 'r') as file:
    SECRET_KEY = file.readline().strip()

assert (SECRET_KEY and SECRET_KEY != '')

SQLALCHEMY_DATABASE_URI = f'sqlite:///{current_dir}/db.sqlite'

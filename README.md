# Simple Todo Website (for BRACU CSE470 Project)

Make sure that SQLite 3 is installed.

Install the following Python libraries: `flask`, `flask-sqlalchemy`, `flask-login`, `db-sqlite3`.

It can be done by typing in `pip install flask flask-sqlalchemy flask-login` into your terminal.

For the project to work, please create a `secret.txt` file containing a secret key (for example,
you could place `f3cfe9ed8fae309f02079dbf`). `config.py` uses the first line of `secret.txt` to get the secret key.
The rest of the lines are ignored.

To run the server, go to terminal and type in the following after `cd`-ing to the project's
parent directory (for Unix-based systems):
```bash
export FLASK_APP=cse470-project
export FLASK_DEBUG=1
flask run
```

In particular, the following should be enough for the entire process (for Mac/Linux):
```bash
# setup
pip install flask flask-sqlalchemy flask-login
git clone https://github.com/ruhanhabib39/cse470-project.git 
echo 'f3cfe9ed8fae309f02079dbf` >> ./cse470-project/secret.txt

# run

export FLASK_APP=cse470-project
export FLASK_DEBUG=1
flask run
```

For Windows, install SQLite 3 and type out the following in cmd:
```batch
pip install flask flask-sqlalchemy flask-login
git clone https://github.com/ruhanhabib39/cse470-project.git 
cd cse470-project
echo 'f3cfe9ed8fae309f02079dbf` >> secret.txt
cd ..

set FLASK_APP=cse470-project
set FLASK_DEBUG=1
flask run
```

The commands above should work, but they have not been tested.


# Simple Todo Website (for BRACU CSE470 Project)

Make sure that SQLite 3 is installed.

Install the following Python libraries: `flask`, `flask-sqlalchemy`, `flask-login`, `db-sqlite3`.

It can be done by typing in `pip install flask flask-sqlalchemy flask-login db-sqlite3` into your terminal.

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


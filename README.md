# Simple Todo Website (for BRACU CSE470 Project)

Make sure that SQLite 3 is installed.

Install the following Python libraries: `flask`, `flask-sqlalchemy`, and `flask-login`.

It can be done by typing in `pip install flask flask-sqlalchemy flask-login` into your terminal.


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

# run

export FLASK_APP=cse470-project
export FLASK_DEBUG=1
flask run
```

For Windows, install SQLite 3 and type out the following in cmd:
```batch
pip install flask flask-sqlalchemy flask-login
git clone https://github.com/ruhanhabib39/cse470-project.git 

set FLASK_APP=cse470-project
set FLASK_DEBUG=1
flask run
```

The commands above should work, but they have not been tested.


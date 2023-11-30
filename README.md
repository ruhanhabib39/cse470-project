# Simple Todo Website (for BRACU CSE470 Project)

Make sure that SQLite 3 is installed.

The following should be enough to setup the project:

For Unix (bash or zsh):
```bash
git clone https://github.com/ruhanhabib39/cse470-project.git
mv cse470-project project
cd project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows (cmd):
```batch
git clone https://github.com/ruhanhabib39/cse470-project.git
ren cse470-project project
cd cse470-project
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

The commands above clones the project, renames the project folder, creates and activates the virtual
environment, and installs the required packages in the virtual directory.

To run the project:
   - cd into the project folder
   - activate the virtual environment (by `source venv/bin/activate` or `venv/Scripts/activate.bat`)
   - and run `python run.py`

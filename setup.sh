#!/bin/bash

git clone https://github.com/ruhanhabib39/cse470-project.git
mv cse470-project project

cd project
python -m venv ./venv

source venv/bin/activate
pip install  -r requirements.txt


deactivate

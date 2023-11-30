#!/bin/bash

source venv/bin/activate

cd ..

export FLASK_APP=project
export FLASK_DEBUG=1
flask run


#!/usr/bin/env bash

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

mkdir db

export FLASK_APP=chat.py

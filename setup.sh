#!/usr/bin/env bash

pip install -r requirements.txt

mkdir db

export FLASK_APP=chat.py

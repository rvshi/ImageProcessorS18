#!/bin/bash
cd backend
export FLASK_APP=main.py
export FLASK_DEBUG=1
../venv/bin/flask run

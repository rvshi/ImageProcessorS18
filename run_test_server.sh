#!/bin/bash
cd backend
gunicorn --bind 0.0.0.0:5000 main:app

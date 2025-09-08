#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Compile messages"
python manage.py compilemessages

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 website.wsgi

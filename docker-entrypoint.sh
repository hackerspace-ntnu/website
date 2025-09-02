#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Compile messages
echo "Compile messages"
python manage.py compilemessages

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 website.wsgi

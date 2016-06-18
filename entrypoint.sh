#!/bin/bash
printenv > /etc/environment
cd /code/
sleep 10
python manage.py migrate
exec gunicorn website.wsgi:application --log-file=/gunicorn-logfiles/error.log --access-logfile=/gunicorn-logfiles/access.log --log-level INFO -w 2 -b :8000

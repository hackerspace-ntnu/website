# Hackerspace Website

The code running [potet.hackerspace-ntnu.no](http://potet.hackerspace-ntnu.no).

## Getting started developing

Install pip3:
`apt-get install python3-pip`

Install required packages for Pillow(Python Image Library):
`sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk`

Clone the project:
`git clone https://github.com/hackerspace-ntnu/website.git`

Install postgresql:
`sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib`

Install virtualenv:
`pip3 install virtualenv`

Create virtualenv:
`virtualenv venv`

Activate virtualenv:
`source venv/bin/activate`

Go into the project:
`cd website/`

Install requirements:
`pip install -r requirements.txt`

####Now its time to setup the database

Change to postgres user:
`sudo su - postgres`

Open database:
`psql`

Create the new database:
`CREATE DATABASE hsdb;`

Create user for the database:
`CREATE USER hackerspace WITH PASSWORD 'password';`

Grant access to the user just created:
`GRANT ALL PRIVILEGES ON DATABASE hsdb TO hackerspace;`

Exit the database:
`\q`

Exit postgres user session:
`exit`

Create local_settings.py:
`vim local_settings.py`
and add the follow values:
- SECRET_KEY = ""
- DEBUG = True
- DOOR_KEY = ''
- EMAIL_HOST_USER = 'web.hackerspace.ntnu@gmail.com'
- EMAIL_HOST_PASSWORD = ''
- DATABASE_USERNAME = 'hackerspace'
- DATABASE_PASSWORD = ''

Make migrations for the database:
`python manage.py makemigrations`

Migrate the database:
`python manage.py migrate`

Run the server:
`python manage.py runserver`







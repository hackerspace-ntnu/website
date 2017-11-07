# Hackerspace Website
[![Build Status](https://travis-ci.org/hackerspace-ntnu/website.svg?branch=master)](https://travis-ci.org/hackerspace-ntnu/website)

The code running [hackerspace-ntnu.no](http://hackerspace-ntnu.no).

## Getting started developing

#### Install all the requirements

Update the OS:
`sudo apt-get update`

Upgrade the OS:
`sudo apt-get upgrade`

Install pip3:
`apt-get install python3-pip`

Install required packages for Pillow(Python Image Library):
`sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk`

Install postgresql:
`sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib`

#### Download the project

Clone the project:
`git clone https://github.com/hackerspace-ntnu/website.git`

#### Set up the virtualenv

Install virtualenv:
`pip3 install virtualenv`

Create virtualenv:
`virtualenv venv`

Activate virtualenv:
`source venv/bin/activate`

#### Install all python packages

Go into the project:
`cd website/`

Install requirements:
`pip install -r requirements.txt`

Create local_settings.py:
`vim local_settings.py`
and add the following values:
- SECRET_KEY = ""
- DEBUG = True
- DOOR_KEY = ''
- EMAIL_HOST_USER = ''
- EMAIL_HOST_PASSWORD = ''
- DATABASE_USERNAME = ''
- DATABASE_PASSWORD = ''
- ALLOWED_HOSTS = ''

#### Set up the database

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

#### Populate the database

Make migrations for the database:
`python manage.py makemigrations`

Migrate the database:
`python manage.py migrate`

#### Start the server

Run the server:
`python manage.py runserver`

# Hackerspace Website
[![Python Integration](https://github.com/hackerspace-ntnu/website/actions/workflows/integration.yml/badge.svg)](https://github.com/hackerspace-ntnu/website/actions/workflows/integration.yml)

The code running [hackerspace-ntnu.no](http://hackerspace-ntnu.no).

## Prerequisites

To get started developing, make sure you have the correct software installed.

This projects uses Django with Python 3. Make sure you have Python3 and pip3 installed.

### For Linux

```
sudo apt install python3 python3-pip python3-venv
```

### For Windows
Alternatives:
1. Install Python3 manually and use CMD

2. Use an environment such as Cygwin64, select pip3 and python3 during install.

3. Install Linux Subsystem for Windows and install Ubuntu (or other prefered distro) from Windows Store

## Set up a virtual environment with virtualenv

Instead of installing a bunch of python files system-wide, we will use a virtual environment to install the packages in a single folder instead.

### For Linux/Mac

1. Create virtualenv:
   ```
   python3 -m venv NAME_OF_VENV
   ```

2. Activate virtualenv:
   ```
   source NAME_OF_VENV/bin/activate
   ```

### For Windows
1. Create virtualenv:
   ```
   python -m venv NAME_OF_VENV
   ```

2. Activate virtualenv:
   ```
   .\NAME_OF_VENV\Scripts\activate
   ```

## Download and initialize the project

Clone the project:
```
git clone git@github.com:hackerspace-ntnu/website.git
```

Go into the project:
```
cd website/
```

Install required python packages:
```
pip install -r requirements.txt
```

Install pre-commit hooks for automatic code formatting and various code style checks:
```
pre-commit install
```

Migrate the database:
```
python manage.py migrate
```

After installing the required packages and initializing the database, you can run the server with the following command:
```
python manage.py runserver
```

## Fixtures

Use fixtures to add test data to you local development

Load the fixtures:
```
python manage.py loaddata fixtures.json
```

Create new fixtures: 
(Create fixtures if model updates make the fixtures unusable)
```
python manage.py dumpdata -e admin -e auth.Permission -e contenttypes -e sessions --indent=4 > fixtures.json
```

All users have the password: `adminpassword`


## Reset database

You can delete the database locally by deleting the db.sqlite3 file from the root directory

After that you need to migrate the database with
```
python manage.py migrate
```

Follow the above step about fixtures if you want your test data back


## Translations

We have locality for Norwegian and English
To generate new translations in `.po` files run
```
python manage.py makemessages -l nb -l en
```

Add the correct translations in the `msgstr` quotes.
If a translation is not given and the `msgstr` quote is empty, the msgid will be used

To compile the translations and make the translations available run
```
python manage.py compilemessages
```
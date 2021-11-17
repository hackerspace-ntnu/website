# Hackerspace Website
[![Build Status](https://travis-ci.org/hackerspace-ntnu/website.svg?branch=master)](https://travis-ci.org/hackerspace-ntnu/website)
[![Coverage Status](https://coveralls.io/repos/github/hackerspace-ntnu/website/badge.svg?branch=master)](https://coveralls.io/github/hackerspace-ntnu/website?branch=master)

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
git clone https://github.com/hackerspace-ntnu/website.git
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

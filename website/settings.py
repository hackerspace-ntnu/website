from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from os import path as os_path
import os
import sys

#################################
# General 						#
#################################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "DefaultSecretKey"
ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'
SITE_ID = 1

ADMINS = (
	('devops', 'hackerspace-dev@idi.ntnu.no'),
)

# Set some variables if DEBUG == False
if os.environ.get('DEBUG') == 'False':
	DEBUG = False
	SECRET_KEY = os.environ.get('SECRET_KEY')
	DOOR_KEY = os.environ.get('DOOR_KEY')
	ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
else:
	DEBUG = True

#################################
# Installed apps                #
#################################

INSTALLED_APPS = [
	'django.contrib.humanize',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'website',
	'applications',
	'news',
	'door',
	'files',
	'ckeditor',
	'ckeditor_uploader',
	'sekizai',
	'sorl.thumbnail',
	'django_nyt',
	'wiki',
	'wiki.plugins.macros',
	'wiki.plugins.help',
	'wiki.plugins.links',
	'wiki.plugins.images',
	'wiki.plugins.attachments',
	'wiki.plugins.notifications',
	'mptt',
	'authentication',
]

#################################
# Database                      #
#################################

if DEBUG:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': 'database',
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': os.environ.get('POSTGRES_USER'),
			'USER': os.environ.get('POSTGRES_USER'),
			'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
			'HOST': 'database',
			'PORT': '5432',
		}
	}

#################################
# Templates                     #
#################################

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'APP_DIRS': True,
		'DIRS': (os.path.join(BASE_DIR, 'templates/'),),
		'OPTIONS': {
			'context_processors': [
				"django.contrib.auth.context_processors.auth",
				"django.template.context_processors.debug",
				"django.template.context_processors.i18n",
				"django.template.context_processors.media",
				"django.template.context_processors.request",
				"django.template.context_processors.static",
				"django.template.context_processors.tz",
				"django.contrib.messages.context_processors.messages",
				"sekizai.context_processors.sekizai",
			],
			'debug': DEBUG,
		}
	},
]

#################################
# Security                      #
#################################

MIDDLEWARE_CLASSES = [
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
]

#################################
# Static                        #
#################################

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
if not DEBUG:
	STATIC_ROOT = '/code/static'
	MEDIA_ROOT = '/code/media'

CKEDITOR_UPLOAD_PATH = os_path.join(BASE_DIR, 'media/uploads')
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = False

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', ),)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#################################
# Email                         #
#################################

#DEFAULT_FROM_MAIL = 'hackerspace-dev@idi.ntnu.no'
DEFAULT_FROM_MAIL = 'web.hackerspace.ntnu@gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#################################
# Internalization               #
#################################

TIME_ZONE = 'Europe/Oslo'

LANGUAGE_CODE = 'nb'

USE_I18N = True
USE_L10N = True
USE_TZ = True

#################################
# Logging                       #
#################################

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler',
			'include_html': True,
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from os import path as os_path
import os
import sys

#################################
# General                       #
#################################


SECRET_KEY = 'SECRET_KEY'
DB = 'sqlite'
DEBUG = True
ALLOWED_HOSTS = ['*']
DOOR_KEY = 'DOOR_KEY'
RPI_SECRET_KEY = 'RPI_SECRET_KEY'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'
SITE_ID = 1
APPEND_SLASH = True
LOGIN_REDIRECT_URL = '/authentication/login/'
LOGIN_URL = '/authentication/login/'

ADMINS = (
    ('devops', 'hackerspace-dev@idi.ntnu.no'),
)

try:
    from .local_settings import *
except ImportError:
    pass

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
    'django.contrib.flatpages',
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
    'smart_selects',
    'committees',
    'dal',
    'dal_select2',
    'material',
    'rpi',
    'inventory',
]


#################################
# App config                    #
#################################

THUMBNAIL_PRESERVE_FORMAT = True


#################################
# Database                      #
#################################

if DB == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
    STATIC_ROOT = '../static'
    MEDIA_ROOT = '../media'

CKEDITOR_UPLOAD_PATH = os_path.join(BASE_DIR, 'media/uploads')
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Undo', 'Redo'],
            ['Format', 'Styles', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline'],
            ['HorizontalRule', 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['TextColor', 'BGColor', 'Smiley'],
            ['RemoveFormat', 'ShowBlocks', 'Maximize'],
            ['Source']
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#################################
# Email                         #
#################################

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_MAIL = 'hackerspace-dev@idi.ntnu.no'
DEFAULT_FROM_MAIL = 'web.hackerspace.ntnu@gmail.com'
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
USE_TZ = False

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
    }
}


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
    },

    'committees': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
    },
}

DEFAULT_CONFIG = CKEDITOR_CONFIGS

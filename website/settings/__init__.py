from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from os import path as os_path
import os
PROJECT_PATH = os_path.abspath(os_path.split(os_path.dirname(__file__))[0])
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from local_settings import SECRET_KEY, DEBUG, DOOR_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DATABASE_USERNAME,\
    DATABASE_PASSWORD

SECRET_KEY = SECRET_KEY
DEBUG = DEBUG
DOOR_KEY = DOOR_KEY
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
DATABASE_USERNAME = DATABASE_USERNAME
DATABASE_PASSWORD = DATABASE_PASSWORD

DEBUG = False
THUMBNAIL_DEBUG = False
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['potet.hackerspace-ntnu.no','beta.hackerspace-ntnu.no']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hsdb',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Europe/Oslo'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-dk'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
#USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")
CKEDITOR_UPLOAD_PATH = os_path.join(PROJECT_PATH, 'media/uploads')
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = False

BOWER_COMPONENTS_ROOT = os_path.join(PROJECT_PATH, 'static/bower')

BOWER_INSTALLED_APPS = (
    'polymer',
)

#STATIC_ROOT = os_path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static',),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (os_path.join(PROJECT_PATH, 'templates'), os.path.join(BASE_DIR, 'templates')),
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

# Setting this dynamically:
# for template_engine in TEMPLATES:
#    template_engine['OPTIONS']['debug'] = True


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
    'news',
    'door',
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
    'djangobower',
    'django_user_agents',
]
from django import VERSION
if VERSION < (1, 7):
    INSTALLED_APPS.append('south')
else:
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            'class': 'django.utils.log.AdminEmailHandler'
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

WIKI_ANONYMOUS_WRITE = False
WIKI_ANONYMOUS_CREATE = False

# Do not user /accounts/profile as default
#LOGIN_REDIRECT_URL = "/"
from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('wiki:get', kwargs={'path': ''})


try:
    import debug_toolbar  # @UnusedImport
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES) + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS = list(INSTALLED_APPS) + ['debug_toolbar']
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
except ImportError:
    pass


# "Secret" key for the prepopulated db

EMAIL_HOST = '173.194.71.108'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



try:
    from website.settings.local import *
except ImportError:
    pass

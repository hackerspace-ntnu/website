from __future__ import absolute_import, unicode_literals

# -*- coding: utf-8 -*-
import os
from datetime import datetime

#################################
# General                       #
#################################

SECRET_KEY = "SECRET_KEY"
DB = "postgres"
DEBUG = True
ALLOWED_HOSTS = ["*"]
DOOR_KEY = "DOOR_KEY"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = "website.urls"
WSGI_APPLICATION = "website.wsgi.application"
SITE_ID = 1
APPEND_SLASH = True
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/authentication/login"
SOCIAL_AUTH_DATAPORTEN_FEIDE_KEY = None
SOCIAL_AUTH_DATAPORTEN_FEIDE_SECRET = None

ADMINS = (("devops", "hackerspace-dev@idi.ntnu.no"),)

#################################
# Installed apps                #
#################################

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.flatpages",
    "search",
    "sorl.thumbnail",
    "website",
    "applications",
    "news",
    "door",
    "files",
    "ckeditor",
    "ckeditor_uploader",
    "authentication",
    "userprofile",
    "seasonal_events",
    "committees",
    "reservations",
    "django_filters",
    "rest_framework",
    "social_django",
    "inventory",
    "watchlist",
    "projectarchive",
    "markdownx",
    "django_crontab",
    "ordered_model",
]


#################################
# App config                    #
#################################

THUMBNAIL_PRESERVE_FORMAT = False

#################################
# Database                      #
#################################

if DB == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_DATABASE"),  # noqa: F405
            "USER": os.environ.get("DB_USER"),  # noqa: F405
            "PASSWORD": os.environ.get("DB_PASSWORD"),  # noqa: F405
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

#################################
# Models                        #
#################################

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

#################################
# Templates                     #
#################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": (os.path.join(BASE_DIR, "templates/"),),
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                # "sekizai.context_processors.sekizai",
                "website.context_processors.template_imports",
                "website.context_processors.banner_context",
                "website.context_processors.mazemap_location",
            ],
            "debug": DEBUG,
        },
    },
]

#################################
# Security                      #
#################################

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "website.middleware.remove_accept_language.RemoveAcceptLanguageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]


AUTHENTICATION_BACKENDS = [
    "dataporten.social.DataportenFeideOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_DATAPORTEN_FEIDE_SSL_PROTOCOL = True
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ["username", "email"]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"

# Keys defined before local import


SOCIAL_AUTH_DATAPORTEN_FEIDE_EXTRA_DATA = ["fullname", "username"]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "authentication.views.associate_by_email",
    "social_core.pipeline.user.create_user",
    "authentication.views.save_profile",  # <--- set the path to the function
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)


#################################
# Static                        #
#################################


STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
if not DEBUG:
    STATIC_ROOT = "../static"
    MEDIA_ROOT = "../media"

CKEDITOR_UPLOAD_PATH = "ck_uploads"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_BROWSE_SHOW_DIRS = False

CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "-", "Undo", "Redo", "-", "PasteText"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Link",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
            ],
            ["Maximize", "Find", "Replace"],
            [
                "Image",
                "Table",
                "HorizontalRule",
                "Smiley",
                "SpecialChar",
                "PageBreak",
                "Iframe",
            ],
        ],
        "extraPlugins": "blockquote",
    },
    "tos_editor": {
        "width": "100%",
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "-", "Undo", "Redo", "-", "PasteText"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Link",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
            ],
            ["Maximize", "Find", "Replace"],
            [
                "Image",
                "Table",
                "HorizontalRule",
                "Smiley",
                "SpecialChar",
                "PageBreak",
                "Iframe",
                "-",
                "Source",
            ],
        ],
        "fullPage": True,
        "extraPlugins": "blockquote",
        "allowedContent": "h1 h2 h3 h4 p b i strong ul li div (*); a [*](*)",
    },
}

DEFAULT_CONFIG = CKEDITOR_CONFIGS

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

#################################
# Email                         #
#################################

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# DEFAULT_FROM_MAIL = 'hackerspace-dev@idi.ntnu.no'
DEFAULT_FROM_MAIL = "web.hackerspace.ntnu@gmail.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#################################
# Internalization               #
#################################

LOCALE_PATHS = (BASE_DIR + "locale/",)
TIME_ZONE = "Europe/Oslo"

LANGUAGE_CODE = "nb"
LANGUAGES = (
    ("nb", "Norwegian"),
    ("en", "English"),
)

USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_FORMAT = "d. F Y"

#################################
# Logging                       #
#################################

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Null handler will consume all logging to it, acting like /dev/null
        "null": {
            "level": DEBUG,
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        # Removes emails about disallowed hosts. We do not really care about these errors anyway.
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
}


#################################
# Rest Framework                #
#################################
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",)
}

# Random greetings that are displayed to the user on the internalportal page
# Just for fun. The user's first name is formatted in
INTERNALPORTAL_GREETINGS = [
    "Hei, {}",  # zzz
    "Heisann, {}",  # zzzzzz
    "Halla, {}",  # zzzzzzzzzzzzzzzzz
    "Og et rungende tjo-bing til deg, {}!",  # real shit?
    "Husket å skru av ovnen, {}?",
    "Dette er en tilfeldig melding. Plukket tilfeldig, altså. Selve meldingen er ikke tilfeldig generert ved å drive å plukke bokstaver og sånt. Du skjønner hva jeg mener, {}.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit... Oi, vent, dette er jo i produksjon!",
]
#################################
# Website-specific              #
#################################
WORKSHOP_OPEN_DAYS = 5

#################################
# Markdownx                     #
#################################

# Markdownify
MARKDOWNX_MARKDOWNIFY_FUNCTION = "markdownx.utils.markdownify"  # Default function that compiles markdown using defined extensions. Using custom function can allow you to pre-process or post-process markdown text. See below for more info.

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = (
    []
)  # List of used markdown extensions. See below for more info.
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = (
    {}
)  # Configuration object for used markdown extensions

# Markdown urls
MARKDOWNX_URLS_PATH = (
    "/markdownx/markdownify/"  # URL that returns compiled markdown text.
)
MARKDOWNX_UPLOAD_URLS_PATH = "/markdownx/upload/"  # URL that accepts file uploads, returns markdown notation of the image.

# Media path
MARKDOWNX_MEDIA_PATH = datetime.now().strftime(
    "markdownx/%Y/%m/%d"
)  # Path, where images will be stored in MEDIA_ROOT folder

# Image
MARKDOWNX_UPLOAD_MAX_SIZE = 52428800  # 50MB - maximum file size
MARKDOWNX_UPLOAD_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
]  # Acceptable file content types
MARKDOWNX_IMAGE_MAX_SIZE = {
    "size": (500, 500),
    "quality": 90,
}  # Different options describing final image processing: size, compression etc. See below for more info.

# Editor
MARKDOWNX_EDITOR_RESIZABLE = (
    True  # Update editor's height to inner content height while typing
)
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.nl2br",
    "markdown.extensions.smarty",
]
# crontab
CRONJOBS = [
    (
        "0 12 * * 2",
        "website.inventory_late_poker.late_loan_retrieval_poker",
        ">>/tmp/scheduled_job.log",
    )
]

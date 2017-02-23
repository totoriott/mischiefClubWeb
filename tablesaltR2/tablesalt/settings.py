"""
Django settings for tablesalt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


ALLOWED_HOSTS = ['tablesalt.megane-moe.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # TODO: don't this, maybe
    'tablesaltGame',
    'lockdown',
)

LOCKDOWN_PASSWORDS = ('bergamot');

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
    #'lockdown.middleware.LockdownMiddleware',
	'tablesaltGame.middleware.StatsMiddleware',
]

ROOT_URLCONF = 'tablesalt.urls'

WSGI_APPLICATION = 'tablesalt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ADMINS = (
    ('Canon', 'ccyoshi+tablesalt@gmail.com'),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'stereotokyo2ToVY0g7S1'
EMAIL_HOST_USER = 'tablesaltgame'
EMAIL_SUBJECT_PREFIX = '[Mischief Club Error] '
EMAIL_USE_TLS = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
"""
credit goes here for this: https://gist.github.com/ndarville/3452907

Two things are wrong with Django's default `SECRET_KEY` system:

1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`

This snippet
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`

The result is a random and safely hidden `SECRET_KEY`.
"""
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join('.', 'ritsuko.NOCOMMIT')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            import random
            SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % SECRET_FILE)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
STATIC_URL = '/bookshelf/'
STATIC_ROOT = os.path.join(BASE_DIR, "bookshelf").replace('\\','/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'bookshelf'),)

# Deployment settings
# thanks http://wiki.dreamhost.com/Django
# STATICFILES_DIRS = [];
#STATIC_ROOT = "../public/bookshelf";
# DEBUG = False;
#TEMPLATE_DEBUG = False;
#SESSION_COOKIE_SECURE = True;
#CSRF_COOKIE_SECURE = True;
#CSRF_COOKIE_HTTPONLY = True;
#X_FRAME_OPTIONS = 'DENY';

# get the site running with django 1.10; not sure if this is prodworthy
# from http://stackoverflow.com/questions/34298867/django-settings-unknown-parameters-template-debug
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
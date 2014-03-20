# -*- coding: utf-8 -*-
# Django settings for eurosentiment project.
#
#    Copyright 2013 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                       DIT, UPM
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os, sys
PROJECT_ROOT = os.path.dirname(os.path.normpath(os.path.abspath(__file__)+'../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
full_path = lambda *parts: os.path.join(PROJECT_ROOT, *parts)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

from eurosentiment.settings_private import *

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['demos.gsi.dit.upm.es']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/eurosentiment/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/var/www/eurosentiment/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/eurosentiment/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nd2^1xto_tzfbawm0u=@hgy9ue0vre1c^*6uc%#=rs^)26q##2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eurosentiment.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eurosentiment.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/www/eurosentiment/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'generator',
    'django_languages',
    'south',
    'codemirror',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
    #'version': 1,
    #'disable_existing_loggers': False,
    #'filters': {
        #'require_debug_false': {
            #'()': 'django.utils.log.RequireDebugFalse'
        #}
    #},
    #'handlers': {
        #'mail_admins': {
            #'level': 'ERROR',
            #'filters': ['require_debug_false'],
            #'class': 'django.utils.log.AdminEmailHandler'
        #},
        #'logfile': {
            #'level': 'ERROR',
            #'class': 'logging.handlers.WatchedFileHandler',
            #'filename': '/var/www/eurosentiment/errors.log'
        #}
    #},
    #'loggers': {
        #'django.request': {
            #'handlers': ['mail_admins', 'logfile'],
            #'level': 'ERROR',
            #'propagate': True,
        #},'marlgenerator': {
            #'handlers': ['logfile'],
            #'level': 'WARNING',
            #'propagate': False
        #},
    #}
#}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        #'null': {
            #'level':'DEBUG',
            #'class':'django.utils.log.NullHandler',
        #},
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            #'filename': PROJECT_ROOT + "/eurosentiment.log",
            'filename': '/var/www/eurosentiment/logs/errors.log',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile'],
            'propagate': False,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'eurosentiment': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['default']['NAME'] = full_path('test.db')
    MEDIA_ROOT = "%s/tmp/" % MEDIA_ROOT

"""
Django settings for ycp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


import os
import socket
from datetime import datetime, timedelta

# import sensitive information
from settings_secret import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() == 'Nnodukas-MacBook-Pro.local':
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = True

ADMINS = (
    ('Noddy', 'nceruchalu@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['www.consortiumforprogress.com', 'consortiumforprogress.com',
                 'www.ycpconsortium.org', 'ycpconsortium.org',
                 'ycp.nceruchalu.webfactional.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.comments',
    'imagekit',
    'haystack',
    'taggit',
    'ycp.apps.media',
    'ycp.apps.youtube',   # could have been called video I guess
    'ycp.apps.photo',
    'ycp.apps.ckeditor',
    'ycp.apps.blog',
    'ycp.apps.comments',  # to customize django comments
    'ycp.apps.tag',       # extends taggit
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ycp.urls'

WSGI_APPLICATION = 'ycp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASES_MYSQL_NAME,
        'USER': DATABASES_MYSQL_USER,
        'PASSWORD': DATABASES_MYSQL_PASSWORD,
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SITE_ID = 1
# SITE_DOMAIN should be consortiumforprogress.com
# using this to reduce the Sites framework db calls
# ref: http://stackoverflow.com/a/8981537
SITE_DOMAIN = 'ycp.nceruchalu.webfactional.com'
SITE_URL = 'http://'+SITE_DOMAIN

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/') #''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = SITE_URL + "/media/" #''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
if DEBUG == True:
    STATIC_URL = '/static/'
else:
    STATIC_URL = AWS_STATIC_BUCKET_URL

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static/'),
    os.path.join(os.path.dirname(__file__), 'static/js'),
    os.path.join(os.path.dirname(__file__), 'static/css'),
    os.path.join(os.path.dirname(__file__), 'static/img'),
    os.path.join(os.path.dirname(__file__), 'static/font'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


ROOT_URLCONF = 'ycp.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)


# just adding request context preprocessor... the first 7 are default
# first 7 ccontext processors are default, just adding:
# - request context processor
# - custom context processor with current site's domain
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "ycp.context_processors.site")


# for ability to see debug in templates using wildcards for IP addresses
if DEBUG: 
    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt):
                    return True
            return False
    
    INTERNAL_IPS = glob_list(['127.0.0.1', '192.168.*.*', 
                              'www.consortiumforprogress.com',
                              'consortiumforprogress.com', 
                              'ycp.nceruchalu.webfactional.com'])


# ---------------------------------------------------------------------------- #
# Amazon AWS storage settings
# ---------------------------------------------------------------------------- #
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

if DEBUG == True:
    AWS_STORAGE_BUCKET_NAME = AWS_TEST_MEDIA_BUCKET_URL
else:
    AWS_STORAGE_BUCKET_NAME = AWS_MEDIA_BUCKET_URL

AWS_REDUCED_REDUNDANCY = True
expires=datetime.now() + timedelta(days=365)
AWS_HEADERS = {
    'Expires':expires.strftime('%a, %d %b %Y 20:00:00 GMT'),
}

# access files from amazon cloudfront (requires using s3boto storage backend)
if DEBUG == True:
    AWS_S3_CUSTOM_DOMAIN = AWS_TEST_MEDIA_CLOUDFRONT_URL
else:
    AWS_S3_CUSTOM_DOMAIN = AWS_MEDIA_CLOUDFRONT_URL 


# ---------------------------------------------------------------------------- #
# search engine (haystack) settings
# ---------------------------------------------------------------------------- #
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__),'whoosh/ycp_index'),
        'INCLUDE_SPELLING': True, # include spelling suggestions
        },
}


# ---------------------------------------------------------------------------- #
# Email settings
# ---------------------------------------------------------------------------- #
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# rest of the settings are in settings_secret.py


# ---------------------------------------------------------------------------- #
# YouTube Settings
# ---------------------------------------------------------------------------- #
# See http://gdata.youtube.com/schemas/2007/categories.cat
YOUTUBE_UPLOAD_CATEGORY = {'term':'Nonprofit','label':'Nonprofits & activisim'}
YOUTUBE_UPLOAD_KEYWORDS = 'ycp, nonprofit'
# other settings in settings_secret.py


# ---------------------------------------------------------------------------- #
# Authentication Settings
# ---------------------------------------------------------------------------- #
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


# ---------------------------------------------------------------------------- #
# CKEditor settings
# ---------------------------------------------------------------------------- #
# see here for full toolbar configs: http://nightly.ckeditor.com/13-02-21-09-53/full/samples/plugins/toolbar/toolbar.html
CKEDITOR_UPLOAD_PATH = '/ckeditor/'
CKEDITOR_CONFIG = {
    'skin': 'moono',
    'height': 291, # pixels or em : '25em' or '300px' or 300
    'width': '100%', # pixels or percent : 300 or '75%'
    'resize_dir':'vertical',
    'removePlugins':'elementspath, flash, iframe', # 'elementspath,resize',
    'extraPlugins':'youtube',
    'toolbar': [
        {'name': 'document',
         'items': ['Save', 'Preview', '-', 'Templates']},
        {'name': 'clipboard',
         'items': ['Cut', 'Copy', 'Paste','PasteText', 'PasteFromWord', '-', 
                   'Undo', 'Redo']},
        {'name': 'editing', 'items': ['Find', 'Replace', '-', 'Scayt']},
        {'name': 'styles', 'items':['Format', 'FontSize']},
	{'name': 'colors', 'items': [ 'TextColor', 'BGColor']},
        '/',
        {'name': 'basicstyles', 
         'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                   'Superscript', '-', 'RemoveFormat']},
        {'name': 'paragraph', 
         'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                   '-', 'Blockquote', '-', 'JustifyLeft', 'JustifyCenter',
                   'JustifyRight', 'JustifyBlock']},
        {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
        {'name': 'insert',
         'items': ['Image', 'youtube', 'HorizontalRule', 'SpecialChar']}
        ],
    'fontSize_defaultLabel':'14px',
    'contentsCss': [STATIC_URL+'ckeditor/contents.css',
                    'http://fonts.googleapis.com/css?family=Raleway:300,700',
                    STATIC_URL+'css/ckeditor.css']
    }


# ---------------------------------------------------------------------------- #
# Django Comments settings
# ---------------------------------------------------------------------------- #
COMMENTS_APP = 'ycp.apps.comments' # app that extends django comments


# ---------------------------------------------------------------------------- #
# imagekit settings
# ---------------------------------------------------------------------------- #
# create appropriate thumbnails on source file save only
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY ='imagekit.cachefiles.strategies.Optimistic'
IMAGEKIT_CACHEFILE_DIR = 'cache'
IMAGEKIT_SPEC_CACHEFILE_NAMER ='imagekit.cachefiles.namers.source_name_as_path'


# ---------------------------------------------------------------------------- #
# general settings
# ---------------------------------------------------------------------------- #
COMMENTS_PER_PAGE = 10 # number of comments per pagination page
MEDIA_PER_PAGE = 21 # number of thumbnails per gallery page (multiple of 3)
ARCHIVES_MONTHS_PER_PAGE = 12 # start with 1 year worth of archives
RESULTS_PER_PAGE = 20 # number of media/post items on a search/tag results page
POSTS_PER_PAGE = RESULTS_PER_PAGE
CONTACT_EMAIL = 'info@'+SITE_DOMAIN # email contact form will reach out to



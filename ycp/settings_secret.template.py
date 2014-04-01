"""
Secret Django settings for ycp project.

Contains sensitive information to be used in Django's settings.py

This file is not to be shared publicly
"""
# Default database credentials
DATABASES_MYSQL_NAME = 'mysql_db_name' 
DATABASES_MYSQL_USER = 'mysql_db_username'
DATABASES_MYSQL_PASSWORD = 'mysql_db_password'



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'generated_by_django'


# AWS properties
AWS_ACCESS_KEY_ID             = 'Amazon Web Services access key'
AWS_SECRET_ACCESS_KEY         = 'Amazon Web Services secret access key'
AWS_STATIC_BUCKET_URL         = 'AWS static files S3 bucket name'

AWS_TEST_MEDIA_BUCKET_URL     = 'AWS media files S3 bucket name, for testing'
AWS_MEDIA_BUCKET_URL          = 'AWS media files S3 bucket name, for production'

AWS_TEST_MEDIA_CLOUDFRONT_URL = 'AWS CDN linked to AWS test media S3 bucket'
AWS_MEDIA_CLOUDFRONT_URL    = 'AWS CDN linked to AWS production media S3 bucket'


# Email settings
# reference: https://docs.djangoproject.com/en/1.6/ref/settings/
EMAIL_HOST          = 'host to use for sending email'
EMAIL_HOST_USER     = 'username to use for the SMTP server' 
EMAIL_HOST_PASSWORD = 'password to use for the SMTP server'
DEFAULT_FROM_EMAIL  = 'webmaster@localhost'
SERVER_EMAIL        = 'root@localhost'


# YouTube settings
YOUTUBE_AUTH_EMAIL = 'sample.email@gmail.com'
YOUTUBE_AUTH_PASSWORD = 'gmail_password'
YOUTUBE_DEVELOPER_KEY = 'YouTube Developer Key'
YOUTUBE_CLIENT_ID = 'YouTube Client ID'

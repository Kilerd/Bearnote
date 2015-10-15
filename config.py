# -*- coding: utf-8 -*-
import os

# Use the ABS path for the project
_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
CSRF_ENABLED = True
SECRET_KEY = '123456'


# Flask-Mail SMTP Setting··
MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEBUG = False


# Mongodb Setting / MongoEngine
MONGODB_DB = os.environ.get('MONGODB_DB', 'bearnote')
MONGODB_HOST = os.environ.get('MONGODB_HOST', '127.0.0.1')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', '')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')

# Unkown What it is.
THREADS_PER_PAGE = 8

# CSRF
CSRF_ENABLED = True
CSRF_SESSION_KEY = "123456"

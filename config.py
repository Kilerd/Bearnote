import os

# Use the ABS path for the project
_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
CSRF_ENABLED = True
SECRET_KEY = '123456'


# Mongodb Setting / MongoEngine
try:
	os.environ['CODING_TEST']
except:
	MONGODB_DB = 'flask'
	MONGODB_HOST = '127.0.0.1'
	MONGODB_PORT = 27017
	MONGODB_USERNAME = 'admin2'
	MONGODB_PASSWORD = 'admin2'
else:
	MONGODB_DB = '1b814d16-7a94-4d2b-8be4-dd594cb82456'
	MONGODB_HOST = '10.9.27.25'
	MONGODB_PORT = 27017
	MONGODB_USERNAME = '773085b7-1b05-452f-911b-56ac72f7b7b1'
	MONGODB_PASSWORD = '0NwMkrE5jWrM3gZ1kZ_yZw'

# Unkown What it is.
THREADS_PER_PAGE = 8

# CSRF
CSRF_ENABLED = True
CSRF_SESSION_KEY = "123456"


# Unkown What it is.
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}
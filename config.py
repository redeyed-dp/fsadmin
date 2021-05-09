from os import urandom;

CSRF_ENABLED = True
SECRET_KEY = urandom(24).hex()

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#BOOTSTRAP_USE_MINIFIED = False
#BOOTSTRAP_SERVE_LOCAL = True
BOOTSTRAP_QUERYSTRING_REVVING = True

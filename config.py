import os
basedir = os.path.abspath(os.path.dirname(__file__))

WEIGHT_UNIT = 'g'
# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
DATABASE_FILE = 'cedar.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_FILE)
SQLALCHEMY_ECHO = False # Print SQL into logs

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

FLASK_ADMIN_SWATCH = 'cosmo'

# 10 mins buffer between shifts.
PRODUCTION_TIME_SHIFT_BUFFER_IN_SEC = 600

# APScheduler
SCHEDULER_VIEWS_ENABLED = True
JOBS = [
    {
        'id': 'test_job',
        'func': 'app.scheduler:test_job',
        'args': (1, 2),
        'trigger': 'interval',
        'seconds': 6000
    },
    {
        'id': 'archive_orders_job',
        'func': 'app.scheduler:archive_orders_job',
        'args': (),
        'trigger': 'interval',
        'seconds': 3
    }
]
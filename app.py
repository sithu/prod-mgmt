"""
New App startup file.

How to run: flask/bin/python app.py
"""
import os
from flask import Flask, render_template
from logging import Formatter, FileHandler

################ Flask #######################
app = Flask(__name__, static_url_path='')

################ Logger ######################
import logging
file_handler = FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)

################ LoginManager ######################
#from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
login_manager.init_app(app)

################ config.py ####################
# Without multiple env support
# app.config.from_object('config')

# better per env setup
app.config.from_object(os.environ['APP_SETTINGS'])

################ DB ####################
# TODO: disable in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

################ Flask-APScheduler #################
class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 36000
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True

def job1(a, b):
    print(str(a) + ' ' + str(b))

from flask_apscheduler import APScheduler
scheduler = APScheduler()
app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()


# product table
from app.models import User
from app.models import product
from app.models import raw_material
from app.models import Order
from app.models import ProductionEntry
from app.models import Machine
from app.models import MachineMold
from app.models import MachineQueue
from app.models import Shift
from app.models import Schedule
from app.routes import index

from app.routes import Users
from app.routes import products
from app.routes import raw_materials
from app.routes import Orders
from app.routes import Productionentries
from app.routes import Machines
from app.routes import Machinemolds
from app.routes import Machinequeues
from app.routes import Shifts
from app.routes import Schedules


if __name__ == '__main__':
	app.run()
############# Deprecated: See@app.py #################
import os
from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__, static_url_path='')

# Without multiple env support
#app.config.from_object('config')
# better per env setup
app_setting = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
print "APP_SETTINGS=%s" % app_setting

app.config.from_object(app_setting)
# TODO: disable in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# def create_app(config_name):
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

login_manager.init_app(app)

from app.models import Product
from app.models import RawMaterial
from app.models import Order
from app.models import ProductionEntry
from app.models import Machine
from app.models import MachineMold
from app.models import MachineQueue
from app.models import Shift
from app.models import Schedule
from app.models import User
from app.models import Color
from app.routes import index

from app.routes import Products
from app.routes import raw_materials
from app.routes import Orders
from app.routes import Productionentries
from app.routes import Machines
from app.routes import Machinemolds
from app.routes import Machinequeues
from app.routes import Shifts
from app.routes import Schedules
from app.routes import Users
from app.routes import Colors

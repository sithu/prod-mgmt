"""
New App startup file.

How to run: flask/bin/python run.py
"""
import os
from flask import Flask, render_template
from logging import Formatter, FileHandler
from app.view import ColorModelView, MachineModelView, ProductModelView
from app import app, admin, db
from flask_admin.consts import ICON_TYPE_GLYPH
from app.model import Color, Machine, Product

################ Flask Admin Setup #######################
admin.add_view(MachineModelView(Machine, db.session, menu_class_name='machine', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-star'))
admin.add_view(ColorModelView(Color, db.session, menu_class_name='color', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-star'))
admin.add_view(ProductModelView(Product, db.session, menu_class_name='product', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-star'))

################ Logger ######################
#import logging
#file_handler = FileHandler('app.log')
#file_handler.setLevel(logging.DEBUG)
#file_handler.setFormatter(
#        Formatter('%(asctime)s %(levelname)s: %(message)s'))
#app.logger.addHandler(file_handler)

################ LoginManager ######################
#from flask.ext.bootstrap import Bootstrap
#from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.login import LoginManager

#login_manager = LoginManager()
#login_manager.session_protection = 'strong'
#login_manager.login_view = 'auth.login'

#from app.auth import auth as auth_blueprint
#app.register_blueprint(auth_blueprint, url_prefix='/auth')
#login_manager.init_app(app)

################ config.py ####################
# Without multiple env support
# app.config.from_object('config')

# better per env setup
app.config.from_object(os.environ['APP_SETTINGS'])

# set flask admin swatch
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

################ DB ####################
# TODO: disable in production
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)

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

# Drop and create DB
db.drop_all()
db.create_all()

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
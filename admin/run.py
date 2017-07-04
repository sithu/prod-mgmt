"""
New App startup file.

How to run: flask/bin/python run.py
"""
import os
import os.path as op
from flask import Flask, render_template
from logging import Formatter, FileHandler
from app.view import (
    ShiftModelView, ColorModelView, MachineModelView, ProductModelView, OrderModelView, ProductionEntryModelView
)
from app import app, admin, db
from flask_admin.consts import ICON_TYPE_GLYPH
from flask_admin.contrib.sqla import ModelView
from app.model import Color, Machine, Product, Order, Shift, ProductionEntry

################ Flask Admin Setup #######################
admin.add_view(MachineModelView(Machine, db.session, menu_class_name='machine', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-wrench'))
admin.add_view(OrderModelView(db.session, menu_class_name='order', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-shopping-cart'))
admin.add_view(ProductionEntryModelView(ProductionEntry, db.session, menu_class_name='production_entry', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-list'))
admin.add_view(ProductModelView(Product, db.session, menu_class_name='product', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-th-large'))
admin.add_view(ColorModelView(Color, db.session, menu_class_name='color', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-picture'))
admin.add_view(ShiftModelView(Shift, db.session, menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-time'))
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
app.config.from_object('config')

# better per env setup
# app.config.from_object(os.environ['APP_SETTINGS'])

#app_setting = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
#print "APP_SETTINGS=%s" % app_setting
#app.config['SECRET_KEY'] = 'my-secret'
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['DATABASE_FILE'] = 'admin.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'admin.db')
#print "SQLALCHEMY_DATABASE_URI=%s" % app.config['SQLALCHEMY_DATABASE_URI']
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# set flask admin swatch
#app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

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

app_dir = op.realpath(os.path.dirname(__file__))
database_path = op.join(app_dir, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
    from app.build_db import build_sample_db
    print "No DB file found! Creating a new DB..."
    build_sample_db()


from flask import send_from_directory

@app.route('/static/<path:path>')
def send_dist(path):
    return send_from_directory(os.path.join(app.root_path, 'static'), path)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)
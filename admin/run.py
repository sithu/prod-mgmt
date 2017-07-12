"""
New App startup file.

How to run: flask/bin/python run.py
"""
import os
import os.path as op
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, url_for, redirect
from app.view import (
    ShiftModelView, ColorModelView, MachineModelView, 
    ProductModelView, OrderModelView, ProductionEntryModelView, 
    RoleBasedModelView, UserModelView, RoleModelView,
    TeamRequestModelView, TeamModelView
)
from app import app, admin, db
from flask_admin.consts import ICON_TYPE_GLYPH
from flask_admin.contrib.sqla import ModelView
from app.model import Color, Machine, Product, Order, Shift, ProductionEntry, User, Role, Team, TeamRequest
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask_apscheduler import APScheduler
from flask import send_from_directory
from app.build_db import build_sample_db

################ config.py ####################
app.config.from_object('config')


################ Flask Admin View Setup #######################
admin.add_view(MachineModelView(Machine, db.session, menu_class_name='machine', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-wrench'))
admin.add_view(OrderModelView(Order, db.session, menu_class_name='order', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-shopping-cart'))
admin.add_view(ProductionEntryModelView(ProductionEntry, db.session, menu_class_name='production_entry', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-list'))
admin.add_view(ProductModelView(Product, db.session, menu_class_name='product', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-th-large'))
admin.add_view(ColorModelView(Color, db.session, menu_class_name='color', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-picture'))
admin.add_view(ShiftModelView(Shift, db.session, category='Employee', menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-time'))
admin.add_view(RoleModelView(Role, db.session, category='Employee', menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-lock'))
admin.add_view(UserModelView(User, db.session, category='Employee', menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-user'))
admin.add_view(TeamRequestModelView(TeamRequest, db.session, category='Employee', menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-random'))
admin.add_view(TeamModelView(Team, db.session, category='Employee', menu_class_name='shift', menu_icon_type=ICON_TYPE_GLYPH, menu_icon_value='glyphicon glyphicon-calendar'))
####################### Flask Security ####################
# Initialize the SQLAlchemy data store and Flask-Security.
print "############# Setting Security #############"
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
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

################ Flask-APScheduler #################
def job1(a, b):
    print(str(a) + ' ' + str(b))
    app.logger.info('Scheduler Running:' + str(a) + ' ' + str(b))


###################### Routes ######################
@app.route('/static/<path:path>')
def send_dist(path):
    return send_from_directory(os.path.join(app.root_path, 'static'), path)

@app.route('/')
def index():
    app.logger.info('Redirect to admin home')
    return redirect(url_for('admin.index'))


def init_db_data():
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        print "No DB file found! Creating a new DB..."
        build_sample_db(user_datastore)

def init_logger():
    handler = RotatingFileHandler('cedar-app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    gunicorn_access_handlers = logging.getLogger('gunicorn.access').handlers
    app.logger.handlers.extend(gunicorn_access_handlers)


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        # gunicorn_access_handlers = logging.getLogger('gunicorn.access').handlers
        # handler = logging.StreamHandler()
        # handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        # app.logger.handlers.extend(gunicorn_access_handlers)
        # app.logger.addHandler(handler)
        # app.logger.setLevel(logging.INFO)
        # #init_logger()
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()

if __name__ == '__main__':
    #init_logger()    
    init_db_data()
    app.run(host="0.0.0.0", debug = False)

from flask import Flask, render_template
#from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)


# def create_app(config_name):
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

login_manager.init_app(app)

# product table
from app.models import User
from app.models import product
from app.models import Order
from app.models import raw_material

from app.routes import index
from app.routes import Users
from app.routes import products
from app.routes import raw_materials
from app.routes import Orders

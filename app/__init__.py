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


from app.models import User
from app.routes import index

from app.routes import Users

# def create_app(config_name):
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

login_manager.init_app(app)

import os

from logging import getLogger
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

LOG = getLogger(__name__)

app = Flask(__name__, static_folder='files')
db = SQLAlchemy(app)

####################### Flask Admin #######################
admin = Admin(
    app, 
    name='Popular Plastic', 
    template_mode='bootstrap3',
    category_icon_classes={
        'Employee': 'glyphicon glyphicon-user',
    }
)


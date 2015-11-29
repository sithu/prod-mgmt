from app import app

from flask import Response
from flask.ext.login import LoginManager, UserMixin, login_required


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/secret')
def secret():
	return 'Only authenticated users are allowed!'

from flask import jsonify
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import auth
#from ..models import User
from .forms import LoginForm
from app import app
from app.models import User

'''
@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password.')

	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

'''

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    user = User.User.query.filter_by(email=json_data['email']).first()

    if user and user.verify_password(json_data['password']):
        from flask.ext.login import login_user
        login_user(user, None)
        status = True
    else:
        status = False
        
    return jsonify(result=status)


@app.route('/api/logout')
def logout():
    from flask.ext.login import logout_user
    logout_user()
    return jsonify(result='success')


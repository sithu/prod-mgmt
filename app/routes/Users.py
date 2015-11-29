from app import app, db
from app.models import User
from flask import abort, jsonify, request
import datetime
import json

@app.route('/prodmgmt/Users', methods = ['GET'])
def get_all_Users():
    entities = User.User.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/prodmgmt/Users/<int:id>', methods = ['GET'])
def get_User(id):
    entity = User.User.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/prodmgmt/Users', methods = ['POST'])
def create_User():
    entity = User.User(
        name = request.json['name']
        , email = request.json['email']
        , password = request.json['password']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/prodmgmt/Users/<int:id>', methods = ['PUT'])
def update_User(id):
    entity = User.User.query.get(id)
    if not entity:
        abort(404)
    entity = User.User(
        name = request.json['name'],
        email = request.json['email'],
        password = request.json['password'],
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/prodmgmt/Users/<int:id>', methods = ['DELETE'])
def delete_User(id):
    entity = User.User.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

#### Customize /api/ endpoints

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


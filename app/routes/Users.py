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
        , phone = request.json['phone']
        , password_hash = request.json['password_hash']
        , level = request.json['level']
        , salary = request.json['salary']
        , department = request.json['department']
        , status = request.json['status']
        , start_date = datetime.datetime.strptime(request.json['start_date'][:10], "%Y-%m-%d").date()
        , end_date = datetime.datetime.strptime(request.json['end_date'][:10], "%Y-%m-%d").date()
        , profile_photo_url = request.json['profile_photo_url']
        , last_login_at = datetime.datetime.strptime(request.json['last_login_at'][:10], "%Y-%m-%d").date()
        , modified_at = datetime.datetime.strptime(request.json['modified_at'][:10], "%Y-%m-%d").date()
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
        phone = request.json['phone'],
        password_hash = request.json['password_hash'],
        level = request.json['level'],
        salary = request.json['salary'],
        department = request.json['department'],
        status = request.json['status'],
        start_date = datetime.datetime.strptime(request.json['start_date'][:10], "%Y-%m-%d").date(),
        end_date = datetime.datetime.strptime(request.json['end_date'][:10], "%Y-%m-%d").date(),
        profile_photo_url = request.json['profile_photo_url'],
        last_login_at = datetime.datetime.strptime(request.json['last_login_at'][:10], "%Y-%m-%d").date(),
        modified_at = datetime.datetime.strptime(request.json['modified_at'][:10], "%Y-%m-%d").date(),
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

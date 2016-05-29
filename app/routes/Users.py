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
        , gender = request.json['gender']
        , shift_name = request.json['shift_name']
        , level = request.json['level']
        , salary = request.json['salary']
        , department = request.json['department']
        , status = request.json['status']
        , start_date = datetime.datetime.strptime(request.json['start_date'][:10], "%Y-%m-%d").date()
        , end_date = datetime.datetime.strptime(request.json['end_date'][:10], "%Y-%m-%d").date()
        , profile_photo_url = request.json['profile_photo_url']
        , modified_at = datetime.datetime.now()
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/prodmgmt/Users/<int:id>', methods = ['PUT'])
def update_User(id):
    entity = User.User.query.get(id)
    if not entity:
        abort(404)

    _end_date = None
    if 'end_date' in request.json and request.json['end_date']:
        _end_date = datetime.datetime.strptime(request.json['end_date'][:10], "%Y-%m-%d").date()

    entity = User.User(
        name = request.json['name'],
        email = request.json['email'],
        phone = request.json['phone'],
        # TODO: handle password reset
        # password_hash = request.json['password_hash'],
        gender = request.json['gender'],
        shift_name = request.json['shift_name'],
        level = request.json['level'],
        salary = request.json['salary'],
        department = request.json['department'],
        status = request.json['status'],
        start_date = datetime.datetime.strptime(request.json['start_date'][:10], "%Y-%m-%d").date(),
        end_date = _end_date,
        profile_photo_url = request.json['profile_photo_url'],
        modified_at = datetime.datetime.now(),
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

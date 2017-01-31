from app import app, db
from app.models.Color import Color
from flask import abort, jsonify, request
import datetime
import json

@app.route('/prodmgmt/Colors', methods = ['GET'])
def get_all_Colors():
    entities = Color.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/prodmgmt/Colors/<string:id>', methods = ['GET'])
def get_Color(id):
    entity = Color.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/prodmgmt/Colors', methods = ['POST'])
def create_Color():
    entity = Color(id= request.json['id'], name = request.json['name'])
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/prodmgmt/Colors/<string:id>', methods = ['PUT'])
def update_Color(id):
    entity = Color.query.get(id)
    if not entity:
        abort(404)
    
    entity.name = request.json['name']
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/prodmgmt/Colors/<string:id>', methods = ['DELETE'])
def delete_Color(id):
    entity = Color.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

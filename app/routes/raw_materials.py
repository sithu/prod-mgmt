from app import app, db
from app.models import RawMaterial
from flask import abort, jsonify, request
import datetime
import json

@app.route('/prodmgmt/raw_materials', methods = ['GET'])
def get_all_raw_materials():
    entities = raw_material.Raw_material.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/prodmgmt/raw_materials/<int:id>', methods = ['GET'])
def get_raw_material(id):
    entity = raw_material.Raw_material.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/prodmgmt/raw_materials', methods = ['POST'])
def create_raw_material():
    entity = raw_material.Raw_material(
        name = request.json['name']
        , weight = request.json['weight']
        , count = request.json['count']
        , purchase_price = request.json['purchase_price']
        , color = request.json['color']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/prodmgmt/raw_materials/<int:id>', methods = ['PUT'])
def update_raw_material(id):
    entity = raw_material.Raw_material.query.get(id)
    if not entity:
        abort(404)
    entity = raw_material.Raw_material(
        name = request.json['name'],
        weight = request.json['weight'],
        count = request.json['count'],
        purchase_price = request.json['purchase_price'],
        color = request.json['color'],
        created_at = datetime.datetime.strptime(request.json['created_at'], "%Y-%m-%d").date(),
        updated_at = datetime.datetime.strptime(request.json['updated_at'], "%Y-%m-%d").date(),
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/prodmgmt/raw_materials/<int:id>', methods = ['DELETE'])
def delete_raw_material(id):
    entity = raw_material.Raw_material.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

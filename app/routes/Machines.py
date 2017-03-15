import datetime
import json

from app import app, db
from app.models.Machine import Machine
from flask import abort, jsonify, request


@app.route('/prodmgmt/Machines', methods=['GET'])
def get_all_Machines():
    entities = Machine.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Machines/<string:id>', methods=['GET'])
def get_Machine(id):
    entity = Machine.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Machines', methods=['POST'])
def create_Machine():
    entity = Machine(
        id=request.json['id']
        , name=request.json['name']
        , status=request.json['status']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Machines/<string:id>', methods=['PUT'])
def update_Machine(id):
    print "updating machine id=", id
    entity = Machine.query.get(id)
    if not entity:
        abort(404)

    entity.name = request.json['name']
    entity.status = request.json['status']

    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Machines/<string:id>', methods=['DELETE'])
def delete_Machine(id):
    entity = Machine.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

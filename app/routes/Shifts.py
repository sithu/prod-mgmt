import json

from app import app, db
from app.models import Shift
from flask import abort, jsonify, request


@app.route('/prodmgmt/Shifts', methods=['GET'])
def get_all_Shifts():
    entities = Shift.Shift.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Shifts/<int:id>', methods=['GET'])
def get_Shift(id):
    entity = Shift.Shift.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Shifts', methods=['POST'])
def create_Shift():
    entity = Shift.Shift(
        shift_name=request.json['shift_name']
        , start_time=request.json['start_time']
        , end_time=request.json['end_time']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Shifts/<int:id>', methods=['PUT'])
def update_Shift(id):
    entity = Shift.Shift.query.get(id)
    if not entity:
        abort(404)
    entity = Shift.Shift(
        shift_name=request.json['shift_name'],
        start_time=request.json['start_time'],
        end_time=request.json['end_time'],
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Shifts/<int:id>', methods=['DELETE'])
def delete_Shift(id):
    entity = Shift.Shift.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

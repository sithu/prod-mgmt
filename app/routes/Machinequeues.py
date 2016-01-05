import json

from app import app, db
from app.models import MachineQueue
from flask import abort, jsonify, request


@app.route('/prodmgmt/Machinequeues', methods=['GET'])
def get_all_Machinequeues():
    entities = MachineQueue.MachineQueue.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Machinequeues/<int:id>', methods=['GET'])
def get_MachineQueue(id):
    entity = MachineQueue.MachineQueue.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Machinequeues', methods=['POST'])
def create_MachineQueue():
    entity = MachineQueue.MachineQueue(
        machine_id=request.json['machine_id']
        , work_in_progress=request.json['work_in_progress']
        , slot_1=request.json['slot_1']
        , slot_2=request.json['slot_2']
        , slot_3=request.json['slot_3']
        , slot_4=request.json['slot_4']
        , slot_5=request.json['slot_5']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Machinequeues/<int:id>', methods=['PUT'])
def update_MachineQueue(id):
    entity = MachineQueue.MachineQueue.query.get(id)
    if not entity:
        abort(404)
    entity = MachineQueue.MachineQueue(
        machine_id=request.json['machine_id'],
        work_in_progress=request.json['work_in_progress'],
        slot_1=request.json['slot_1'],
        slot_2=request.json['slot_2'],
        slot_3=request.json['slot_3'],
        slot_4=request.json['slot_4'],
        slot_5=request.json['slot_5'],
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Machinequeues/<int:id>', methods=['DELETE'])
def delete_MachineQueue(id):
    entity = MachineQueue.MachineQueue.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

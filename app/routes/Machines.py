import datetime
import json

from app import app, db
from app.models import Machine
from flask import abort, jsonify, request


@app.route('/prodmgmt/Machines', methods=['GET'])
def get_all_Machines():
    entities = Machine.Machine.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Machines/<int:id>', methods=['GET'])
def get_Machine(id):
    entity = Machine.Machine.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Machines', methods=['POST'])
def create_Machine():
    entity = Machine.Machine(
        name=request.json['name']
        #, supported_mold_type=request.json['supported_mold_type']
        #, installed_mold_id=request.json['installed_mold_id']
        , status=request.json['status']
        #, downtime_start=datetime.datetime.strptime(request.json['downtime_start'][:10], "%Y-%m-%d").date()
        #, downtime_end=datetime.datetime.strptime(request.json['downtime_end'][:10], "%Y-%m-%d").date()
        #, total_downtime=request.json['total_downtime']
        , created_at=datetime.datetime.now()
        , modified_at=datetime.datetime.now()
        , supervisor_attention=request.json['supervisor_attention']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Machines/<int:id>', methods=['PUT'])
def update_Machine(id):
    entity = Machine.Machine.query.get(id)
    if not entity:
        abort(404)
    entity = Machine.Machine(
        name=request.json['name'],
        #supported_mold_type=request.json['supported_mold_type'],
        #installed_mold_id=request.json['installed_mold_id'],
        status=request.json['status'],
        #downtime_start=datetime.datetime.strptime(request.json['downtime_start'][:10], "%Y-%m-%d").date(),
        #downtime_end=datetime.datetime.strptime(request.json['downtime_end'][:10], "%Y-%m-%d").date(),
        #total_downtime=request.json['total_downtime'],
        #created_at=datetime.datetime.strptime(request.json['created_at'][:10], "%Y-%m-%d").date(),
        modified_at=datetime.datetime.now(),
        supervisor_attention=request.json['supervisor_attention'],
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Machines/<int:id>', methods=['DELETE'])
def delete_Machine(id):
    entity = Machine.Machine.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

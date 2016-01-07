import datetime
import json

from app import app, db
from app.models import MachineMold
from flask import abort, jsonify, request


@app.route('/prodmgmt/Machinemolds', methods=['GET'])
def get_all_Machinemolds():
    entities = MachineMold.MachineMold.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Machinemolds/<int:id>', methods=['GET'])
def get_MachineMold(id):
    entity = MachineMold.MachineMold.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Machinemolds', methods=['POST'])
def create_MachineMold():
    entity = MachineMold.MachineMold(
        mold_type=request.json['mold_type']
        , time_to_install=request.json['time_to_install']
        , created_at=datetime.datetime.strptime(request.json['created_at'][:10], "%Y-%m-%d").date()
        , modified_at=datetime.datetime.strptime(request.json['modified_at'][:10], "%Y-%m-%d").date()
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Machinemolds/<int:id>', methods=['PUT'])
def update_MachineMold(id):
    entity = MachineMold.MachineMold.query.get(id)
    if not entity:
        abort(404)
    entity = MachineMold.MachineMold(
        mold_type=request.json['mold_type'],
        time_to_install=request.json['time_to_install'],
        created_at=datetime.datetime.strptime(request.json['created_at'][:10], "%Y-%m-%d").date(),
        modified_at=datetime.datetime.strptime(request.json['modified_at'][:10], "%Y-%m-%d").date(),
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Machinemolds/<int:id>', methods=['DELETE'])
def delete_MachineMold(id):
    entity = MachineMold.MachineMold.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

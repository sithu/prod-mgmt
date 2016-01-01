import datetime
import json
import threading

from app import app, db
from app.models import ProductionEntry
from flask import abort, jsonify, request

lock = threading.RLock()


@app.route('/prodmgmt/Productionentries', methods=['GET'])
def get_all_Productionentries():
    entities = ProductionEntry.ProductionEntry.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Productionentries/<int:id>', methods=['GET'])
def get_ProductionEntry(id):
    entity = ProductionEntry.ProductionEntry.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Productionentries', methods=['POST'])
def create_ProductionEntry():
    print request.json
    entity = ProductionEntry.ProductionEntry(
        status=request.json['status']
        , shift_name=request.json['shift_name']
        , machine_id=request.json['machine_id']
        , raw_material_id=request.json['raw_material_id']
        , order_id=request.json['order_id']
        , team_lead_id=request.json['team_lead_id']
        , team_lead_name=request.json['team_lead_name']
        , estimated_time_to_finish=request.json['estimated_time_to_finish']
        , start=datetime.datetime.strptime(request.json['start'][:10], "%Y-%m-%d").date()
        , end=datetime.datetime.strptime(request.json['end'][:10], "%Y-%m-%d").date()
        , delay=request.json['delay']
        , delay_reason=request.json['delay_reason']
        , planned_quantity=request.json['planned_quantity']
        , finished_quantity=request.json['finished_quantity']
        , defected_quantity=request.json['defected_quantity']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Productionentries/<int:id>', methods=['PUT'])
def update_ProductionEntry(id):
    entity = ProductionEntry.ProductionEntry.query.get(id)
    if not entity:
        abort(404)
    entity = ProductionEntry.ProductionEntry(
        status=request.json['status'],
        shift_name=request.json['shift_name'],
        machine_id=request.json['machine_id'],
        raw_material_id=request.json['raw_material_id'],
        order_id=request.json['order_id'],
        team_lead_id=request.json['team_lead_id'],
        team_lead_name=request.json['team_lead_name'],
        estimated_time_to_finish=request.json['estimated_time_to_finish'],
        start=datetime.datetime.strptime(request.json['start'][:10], "%Y-%m-%d").date(),
        end=datetime.datetime.strptime(request.json['end'][:10], "%Y-%m-%d").date(),
        delay=request.json['delay'],
        delay_reason=request.json['delay_reason'],
        planned_quantity=request.json['planned_quantity'],
        finished_quantity=request.json['finished_quantity'],
        defected_quantity=request.json['defected_quantity'],
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Productionentries/<int:id>', methods=['DELETE'])
def delete_ProductionEntry(id):
    entity = ProductionEntry.ProductionEntry.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204


@app.route('/prodmgmt/Productionentries/<int:id>/defected', methods=['POST'])
def increment_defected_quantity(id):
    """
    Method to increment defected quantity. This method should be used for IoT device interaction.
    :param id: Production Entry ID
    :return:
    """
    lock.acquire();
    try:
        entity = ProductionEntry.ProductionEntry.query.get(id)
        if not entity:
            abort(404)
        # TODO Additional check can be added to check if
        # status is IN_PROGRESS before incrementing quantity
        entity.defected_quantity = entity.defected_quantity + 1;
        db.session.merge(entity)
        db.session.commit()
    finally:
        lock.release()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Productionentries/<int:id>/finished', methods=['POST'])
def increment_finished_quantity(id):
    """
    Method to increment finished quantity. This method should be used for IoT device interaction.
    :param id: Production Entry ID
    :return:
    """
    lock.acquire()
    try:
        entity = ProductionEntry.ProductionEntry.query.get(id)
        if not entity:
            abort(404)
        # TODO Additional check can be added to check if
        # status is IN_PROGRESS before incrementing quantity
        entity.finished_quantity = entity.finished_quantity + 1;
        db.session.merge(entity)
        db.session.commit()
    finally:
        lock.release()
    return jsonify(entity.to_dict()), 200

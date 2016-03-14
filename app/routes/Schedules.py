import datetime
import json

from app import app, db
from app.models import Schedule
from flask import abort, jsonify, request


@app.route('/prodmgmt/Schedules', methods=['GET'])
def get_all_Schedules():
    entities = Schedule.Schedule.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Schedules/<int:id>', methods=['GET'])
def get_Schedule(id):
    entity = Schedule.Schedule.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

'''
@app.route('/prodmgmt/Schedules', methods=['POST'])
def create_Schedule():
    entity = Schedule.Schedule(
        date=datetime.datetime.strptime(request.json['date'][:10], "%Y-%m-%d").date()
        , shift_name=request.json['shift_name']
        , employee_id=request.json['employee_id']
        , manager_id=request.json['manager_id']
        , is_in_duty=request.json['is_in_duty']
        , assigned_machine=request.json['assigned_machine']
        , sign_in_at=datetime.datetime.strptime(request.json['sign_in_at'][:10], "%Y-%m-%d").date()
        , sign_out_at=datetime.datetime.strptime(request.json['sign_out_at'][:10], "%Y-%m-%d").date()
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201
'''

@app.route('/prodmgmt/Schedules/<int:id>', methods=['PUT'])
def update_Schedule(id):
    entity = Schedule.Schedule.query.get(id)
    if not entity:
        abort(404)
    entity = Schedule.Schedule(
        date=datetime.datetime.strptime(request.json['date'][:10], "%Y-%m-%d").date(),
        shift_name=request.json['shift_name'],
        employee_id=request.json['employee_id'],
        manager_id=request.json['manager_id'],
        is_in_duty=request.json['is_in_duty'],
        assigned_machine=request.json['assigned_machine'],
        sign_in_at=datetime.datetime.strptime(request.json['sign_in_at'][:10], "%Y-%m-%d").date(),
        sign_out_at=datetime.datetime.strptime(request.json['sign_out_at'][:10], "%Y-%m-%d").date(),
        id=id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Schedules/<int:id>', methods=['DELETE'])
def delete_Schedule(id):
    entity = Schedule.Schedule.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

@app.route('/prodmgmt/Schedules', methods=['POST'])
def create_Schedule():
    '''
    Modified version of scheduler
    '''
    return jsonify("foo"), 201
    '''
    entity = Schedule.Schedule(
        date=datetime.datetime.strptime(request.json['date'][:10], "%Y-%m-%d").date()
        , shift_name=request.json['shift_name']
        , employee_id=request.json['employee_id']
        , manager_id=request.json['manager_id']
        , is_in_duty=request.json['is_in_duty']
        , assigned_machine=request.json['assigned_machine']
        , sign_in_at=datetime.datetime.strptime(request.json['sign_in_at'][:10], "%Y-%m-%d").date()
        , sign_out_at=datetime.datetime.strptime(request.json['sign_out_at'][:10], "%Y-%m-%d").date()
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201
    '''
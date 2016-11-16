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
    # 1. Gets all available machines
    from app.models.Machine import Machine
    app.logger.debug('Get all available machines')
    machines = Machine.query.filter_by(status='Available').all()
    #app.logger.debug("################")
    #for m in machines:
    #    app.logger.debug(m.status)
    
    # 2. Gets all available employees and supervisors
    from app.models.User import User
    employees = User.query.filter(User.status != 'VACATION').all()
    supervisors = []
    for e in employees:
        if e.level == '4':
            employees.remove(e)
            supervisors.append(e)
            app.logger.debug('Supervisors')
        elif e.level == '5':  
            app.logger.debug('Employee')
        else: 
            app.logger.debug('Not valid to schedule=%s', e.name)

    numEmp = len(employees)
    app.logger.debug("numEmp=%d,numSup=%d", numEmp, len(supervisors))
    import random
    indexes = random.sample(xrange(0, numEmp), numEmp)
    app.logger.debug(indexes)

    # set initail pointers (machine and supervisor)
    curr_machine = machines.pop()
    curr_supervisor = supervisors.pop()
    curr_supervisor_utilization = 100
    curr_assigned_worker_count = 0

    from app.models.Schedule import Schedule
    for i in indexes:
        # machine assignment
        if curr_assigned_worker_count == curr_machine.num_worker_needed:
            curr_machine = machines.pop()
            curr_assigned_worker_count = 0
        
        # supervisor assignment
        if curr_supervisor_utilization >= curr_machine.supervisor_attention:
            curr_supervisor_utilization -= curr_machine.supervisor_attention
        else:
            curr_supervisor = supervisors.pop()
            curr_supervisor_utilization = 100
        
        # worker assignment 
        e = employees[i]
        curr_assigned_worker_count += 1

        # schedule creation TODO: how to assignment shift?
        app.logger.debug(e)
        s = Schedule(
            date=datetime.now(),
            shift_name='M',
            employee_id=e.id,
            lead_id=curr_supervisor.id,
            assigned_machine=1
        )
        app.logger.debug(s.__dict__)


    return "", 201
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
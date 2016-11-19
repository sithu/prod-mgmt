import datetime
import json
import random
       
from flask import abort, jsonify, request
from datetime import datetime

from app import app, db
from app.models import Schedule
from app.models.Machine import Machine
from app.models.User import User
from app.models.Schedule import Schedule


@app.route('/prodmgmt/Schedules', methods=['GET'])
def get_all_Schedules():
    entities = Schedule.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Schedules/<int:id>', methods=['GET'])
def get_Schedule(id):
    entity = Schedule.query.get(id)
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
    entity = Schedule.query.get(id)
    if not entity:
        abort(404)
    entity = Schedule(
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
    entity = Schedule.query.get(id)
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
    app.logger.debug('Get all available machines')
    machines = Machine.query.filter_by(status='Available').all()
    
    # 2. Gets all available employees and supervisors
    all_employees = User.query.filter(User.status != 'VACATION').all()
    app.logger.debug('Num employees=%d', len(all_employees))
    supervisors = []
    employees = []
    # Support one (first from the list) manager only!
    managers = {}
    for e in all_employees:
        app.logger.debug('Name=%s', e.name)
        if e.level == 3: # Manager
            app.logger.debug('Manager Shift=%s', e.shift_name)
            managers[e.shift_name] = e
        elif e.level == 4: # Supervisor
            supervisors.append(e)
        elif e.level == 5: # Employee
            employees.append(e)
    
    app.logger.debug('##### Total Managers = %d #####', len(managers))

    numEmp = len(employees)
    app.logger.debug("numEmp=%d,numSup=%d", numEmp, len(supervisors))
    indexes = random.sample(xrange(0, numEmp), numEmp)
    app.logger.debug(indexes)

    # set initail pointers (machine and supervisor)
    curr_machine = machines.pop()
    curr_supervisor = supervisors.pop()

    curr_supervisor_utilization = 100
    curr_assigned_worker_count = 0

    for i in indexes:
        # machine assignment
        if curr_assigned_worker_count == curr_machine.num_worker_needed:
            if len(machines) == 0:
                # If all machines are assigned, then use a dummy machine.
                curr_machine = Machine(
                    id=None, 
                    name='N/A', 
                    supervisor_attention=25,
                    num_worker_needed=3)
            else:
                curr_machine = machines.pop()
            curr_assigned_worker_count = 0
        
        # supervisor assignment
        if curr_supervisor_utilization >= curr_machine.supervisor_attention:
            curr_supervisor_utilization -= curr_machine.supervisor_attention
        else:
            if len(supervisors) == 0:
                curr_supervisor = managers[e.shift_name]
            else:
                curr_supervisor = supervisors.pop()
            
            curr_supervisor_utilization = 100
        
        # worker assignment 
        e = employees[i]
        curr_assigned_worker_count += 1

        # schedule creation TODO: how to assignment shift?
        s = Schedule(
            date=datetime.now(),
            shift_name=e.shift_name,
            employee_id=e.id,
            lead_id=curr_supervisor.id,
            assigned_machine=curr_machine.id
        )
        #app.logger.debug(s.__dict__)


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
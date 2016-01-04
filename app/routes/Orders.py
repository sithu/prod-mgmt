from app import app, db
from app.models import Order
from flask import abort, jsonify, request
import datetime
import json


@app.route('/prodmgmt/Orders', methods=['GET'])
def get_all_Orders():
    entities = Order.Order.query.all()
    return json.dumps([entity.to_dict() for entity in entities])


@app.route('/prodmgmt/Orders/<int:id>', methods=['GET'])
def get_Order(id):
    entity = Order.Order.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())


@app.route('/prodmgmt/Orders', methods=['POST'])
def create_Order():
    entity = Order.Order(
        status=request.json['status']
        , product_id=request.json['product_id']
        , quantity=request.json['quantity']
        , raw_material_quantity=request.json['raw_material_quantity']
        , created_at=datetime.datetime.strptime(request.json['created_at'][:10], "%Y-%m-%d").date()
        , estimated_time_to_finish=request.json['estimated_time_to_finish']
        , production_start_at=datetime.datetime.strptime(request.json['production_start_at'][:10], "%Y-%m-%d").date()
        , production_end_at=datetime.datetime.strptime(request.json['production_end_at'][:10], "%Y-%m-%d").date()
        , note=request.json['note']
    )
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201


@app.route('/prodmgmt/Orders/<int:id>', methods=['PUT'])
def update_Order(id):
    entity = Order.Order.query.get(id)
    if not entity:
        abort(404)
    entity = Order.Order(
        id=request.json['id'],
        status=request.json['status'],
        product_id=request.json['product_id'],
        quantity=request.json['quantity'],
        raw_material_quantity=request.json['raw_material_quantity'],
        created_at=datetime.datetime.strptime(request.json['created_at'][:10], "%Y-%m-%d").date(),
        estimated_time_to_finish=request.json['estimated_time_to_finish'],
        production_start_at=datetime.datetime.strptime(request.json['production_start_at'][:10], "%Y-%m-%d").date(),
        production_end_at=datetime.datetime.strptime(request.json['production_end_at'][:10], "%Y-%m-%d").date(),
        note=request.json['note'],
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200


@app.route('/prodmgmt/Orders/<int:id>', methods=['DELETE'])
def delete_Order(id):
    entity = Order.Order.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

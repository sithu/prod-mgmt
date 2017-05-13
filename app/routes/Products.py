from app import app, db
from app.models.Product import Product
from app.models.Color import Color
from flask import abort, jsonify, request
import datetime
import json

@app.route('/prodmgmt/products', methods = ['GET'])
def get_all_products():
    app.logger.debug('GET all products from DB...')
    entities = Product.query.all()
    return json.dumps([entity.to_dict() for entity in entities])

@app.route('/prodmgmt/products/<int:id>', methods = ['GET'])
def get_product(id):
    entity = Product.query.get(id)
    if not entity:
        abort(404)
    return jsonify(entity.to_dict())

@app.route('/prodmgmt/products', methods = ['POST'])
def create_product():
    now = datetime.datetime.utcnow()
    entity = Product(
        id=request.json['id']
        , name=request.json['name']
        , created_at=now
        , updated_at=now
        , weight=int(request.json['weight'])
        , time_to_build=int(request.json['time_to_build'])
        , selling_price=int(request.json['selling_price'])
        , num_employee_required=int(request.json['num_employee_required'])
        , mold_id=int(request.json['mold_id'])
        , photo_url=None)
    entity.colors = [Color.query.filter_by(id=c).first() for c in request.json['colors']]
    db.session.add(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 201

@app.route('/prodmgmt/products/<int:id>', methods = ['PUT'])
def update_product(id):
    entity = Product.query.get(id)
    if not entity:
        abort(404)
    entity = Product(
        name = request.json['name'],
        type = request.json['type'],
        weight = request.json['weight'],
        time_to_build = request.json['time_to_build'],
        selling_price = request.json['selling_price'],
        color = request.json['color'],
        created_at = datetime.datetime.strptime(request.json['created_at'], "%Y-%m-%d").date(),
        updated_at = datetime.datetime.strptime(request.json['updated_at'], "%Y-%m-%d").date(),
        mold_id = request.json['mold_id'],
        id = id
    )
    db.session.merge(entity)
    db.session.commit()
    return jsonify(entity.to_dict()), 200

@app.route('/prodmgmt/products/<int:id>', methods = ['DELETE'])
def delete_product(id):
    entity = Product.query.get(id)
    if not entity:
        abort(404)
    db.session.delete(entity)
    db.session.commit()
    return '', 204

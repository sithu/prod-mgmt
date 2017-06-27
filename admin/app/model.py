import enum
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property
from sqlalchemy import select, func

class Base(db.Model):
    """
    Define a base model for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

########################## Models ################################
class Machine(Base):
    __tablename__ = 'machine'
    name = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(db.Enum('OFF', 'ON', 'BUSY', 'BROKEN'), nullable=False)
    power_in_kilowatt = db.Column(db.Integer) 
    photo = db.Column(db.String)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            power_in_kilowatt=self.power_in_kilowatt,
            photo=self.photo,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class Shift(db.Model):
    __tablename__ = 'shift'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    shift_name = db.Column(db.String, nullable=False, unique=True)
    start_hour = db.Column(db.Integer, nullable=False)
    end_hour = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '%s' % (self.shift_name)

    def toAM_PM(self, hour):
        if hour == 12:
            return "12P.M"
        elif hour > 12:
            return "%dP.M" % (hour-12)
        else:
            return "%dA.M" % (hour)


class Color(db.Model):
    """
    class doc
    """
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False, unique=True)
    color_code = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)

#m-m mapping
product_colors_table = db.Table(
    'product_color',
    db.Model.metadata,
    db.Column('product_id', db.String, db.ForeignKey('product.id')),
    db.Column('color_id', db.String, db.ForeignKey('color.id'))
)


class Product(Base):
    '''Model for product table'''
    __tablename__ = 'product'
    name = db.Column(db.String, nullable=False, unique=True)
    weight = db.Column(db.Integer, nullable=False)
    time_to_build = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer, nullable=False)
    raw_material_weight_per_bag = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String)
    multi_colors_ratio = db.Column(db.String)
    colors = db.relationship(Color, secondary=product_colors_table)
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id), nullable=False)
    machine = db.relationship(Machine, backref='machine')

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class ProductionEntry(db.Model):
    __tablename__ = 'production_entry'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    shift_id = db.Column(db.Integer, db.ForeignKey(Shift.id), nullable=False)
    shift = db.relationship(Shift, backref='production_entry_shift')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref='production_entry_orders')
    team_lead_name = db.Column(db.String)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    num_hourly_good = db.Column(db.String, default='')
    num_hourly_bad = db.Column(db.String, default='')
    num_good = db.Column(db.Integer, default=0)
    num_bad = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum('NEW', 'IN_PROGRESS', 'CLOSED'), nullable=False, default='NEW')
    
        
    @hybrid_property
    def machine_id(self):
        return self.order.assigned_machine_id
    
    @hybrid_property
    def photo(self):
        return self.order.photo

    def save(self, *args, **kwargs):
        print "override save method"
        self.order.production_entries.append(self)
        return super(ProductionEntry, self).save(*args, **kwargs)


class Order(db.Model):
    """Order table ORM mapping"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('AUTO_PLAN', 'MANUAL_PLAN', 'IN_PROGRESS', 'COMPLETED', 'SHIPPED'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    quantity_completed = db.Column(db.Integer, default=0)
    current_quantity_completed = db.Column(db.Integer, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, backref='product')
    raw_material_quantity = db.Column(db.Integer, nullable=False, default=0)
    estimated_time_to_complete = db.Column(db.Integer, nullable=False)
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    assigned_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    # NOTE: backref name MUST be unique between relationships.
    assigned_machine = db.relationship(Machine, backref='order_to_machine')
    # 1-m mapping
    production_entries = relationship(
        'ProductionEntry', backref='order_to_production_entries'
    )
    completed = column_property(
        select([func.sum(ProductionEntry.num_good)]).\
            where(ProductionEntry.order_id==id).\
            correlate_except(ProductionEntry)
    )

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


    @hybrid_property
    def photo(self):
        return self.product.photo

 
############ ORM Triggers #############
from sqlalchemy.event import listens_for
from decimal import *

@listens_for(Order, 'before_insert')
def before_order_insert(mapper, connection, target):
    print "%%%%%%%% before_insert_order %%%%%%%%%%"
    # 1. Calculate number of raw material bags.
    product = Product.query.get(target.product_id)
    weight = Decimal(product.weight)
    total_weight = Decimal(target.quantity) * weight
    num_raw_bag = Decimal(total_weight) / product.raw_material_weight_per_bag
    # round results to fixed number
    target.raw_material_quantity = int(Decimal(num_raw_bag).quantize(Decimal('1.'), rounding=ROUND_UP))
    print "1. num_raw_bag = %d" % target.raw_material_quantity

    # 2. Calculate estimated time to complete
    target.estimated_time_to_complete = target.quantity * product.time_to_build
    print "2. Estimated time to complete = %d sec" % target.estimated_time_to_complete
    
    # 3. Set the mode based on the machine id is default or not.
    target.status = 'MANUAL_PLAN'
    if not target.assigned_machine_id:
        target.assigned_machine_id = product.machine_id
        target.status = 'AUTO_PLAN'
    

@listens_for(Order, 'before_update')
def before_order_update(mapper, connection, target):
    print "%%%%%%%% before_update_order %%%%%%%%%%"
    # 1. Calculate number of raw material bags.
    
    for s in ('IN_PROGRESS', 'COMPLETED', 'SHIPPED'):
        if target.status == s:
            print "Invalid state. Changes cannot be made."

    if target.quantity_completed + target.current_quantity_completed >= target.quantity:
        target.status = 'COMPLETED'
        target.production_end_at = db.func.current_timestamp()
        print "Order completed"

    if target.assigned_machine_id is not target.product.machine_id:
        target.status = 'MANUAL_PLAN'


@listens_for(ProductionEntry, 'before_insert')
def before_production_entry_insert(mapper, connection, target):
    print "========== before_production_entry_insert ========="
    print dir(target)
    #order = Order.query.get(target.order_id)
    #updated_entries = order.production_entries
    #updated_entries.append(target)
    #Order.query.filter_by(id=target.order_id).update({ 'production_entries': updated_entries })
    print "appended new production entry"


@listens_for(ProductionEntry, 'before_update')
def before_productionentry_update(mapper, connection, target):
    print "========== before production entry update ========="
    from datetime import datetime
    now = datetime.now()

    if target.num_hourly_good:
        num_good = sum([int(x) for x in target.num_hourly_good.split(',')])
        target.num_good = num_good
    
    if target.num_hourly_bad:
        num_bad = sum([int(x) for x in target.num_hourly_bad.split(',')])
        target.num_bad = num_bad

    if target.status == 'IN_PROGRESS':
        if target.start is None:
            # Record start time if unset.
            target.start = now

        order = Order.query.get(target.order_id)
        if order.status != 'IN_PROGRESS':
            order.status = 'IN_PROGRESS'
            Order.query.filter_by(id=target.order_id).update({ 'status': 'IN_PROGRESS', 'production_start_at': now})
        
        if target.num_hourly_good:
            order_update = {}
            order_update['current_quantity_completed'] = num_good
            num_completed = num_good + order.quantity_completed
            if num_completed >= order.quantity:
                target.status = 'CLOSED'
                target.end = now
                order_update['status'] = 'COMPLETED'
                order_update['production_end_at'] = now
                order_update['quantity_completed'] = num_completed
                order_update['current_quantity_completed'] = 0
            Order.query.filter_by(id=target.order_id).update(order_update)
    elif target.status == 'CLOSED':
        target.end = db.func.current_timestamp()
        order = Order.query.get(target.order_id)
        order.current_quantity_completed = 0
        if target.num_hourly_good:
            order.quantity_completed += num_good
    else:
        print "NEW status. Do nothing"

        

    
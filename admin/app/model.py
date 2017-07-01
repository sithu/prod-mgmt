import enum
from app import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from datetime import datetime, date

    
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
    status = db.Column(db.Enum('OFF', 'ON', 'BROKEN'), nullable=False)
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
    num_hourly_good = db.Column(db.String, default='')
    num_hourly_bad = db.Column(db.String, default='')
    num_good = db.Column(db.Integer, default=0)
    num_bad = db.Column(db.Integer, default=0)
    date = Column(Date, default=date.today())

    @hybrid_property
    def machine_id(self):
        return self.order.assigned_machine_id
    
    @hybrid_property
    def photo(self):
        return self.order.photo

    @hybrid_property
    def product_colors(self):
        return self.order.product_colors

    @hybrid_property
    def status(self):
        return self.order.status

    @hybrid_property
    def remaining(self):
        return self.order.remaining

    def save(self, *args, **kwargs):
        print "FIXME: override save method"
        self.order.production_entries.append(self)
        return super(ProductionEntry, self).save(*args, **kwargs)


class Order(db.Model):
    """Order table ORM mapping"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('NEW', 'IN_PROGRESS', 'COMPLETED'), nullable=False, default='NEW')
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, backref='product')
    raw_material_quantity = db.Column(db.Integer, nullable=False, default=0)
    estimated_time_to_complete = db.Column(db.Integer, nullable=False)
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    assigned_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    # NOTE: backref name MUST be unique between relationships.
    assigned_machine = db.relationship(Machine, backref=db.backref('order_to_machine', uselist=False))
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

    @hybrid_property
    def product_colors(self):
        return self.product.colors

    @hybrid_property
    def remaining(self):
        return self.quantity - self.completed


############ ORM Triggers #############
from sqlalchemy.event import listens_for
from decimal import *

def calculate_order_details(target):
    # 1. Calculate number of raw material bags.
    product = Product.query.get(target.product_id)
    weight = Decimal(product.weight)
    total_weight = Decimal(target.quantity) * weight
    num_raw_bag = Decimal(total_weight) / product.raw_material_weight_per_bag
    # round results to fixed number
    target.raw_material_quantity = int(Decimal(num_raw_bag).quantize(Decimal('1.'), rounding=ROUND_UP))
    
    # 2. Calculate estimated time to complete
    target.estimated_time_to_complete = target.quantity * product.time_to_build

    # 3. Set the mode based on the machine id is default or not.
    if not target.assigned_machine_id:
        target.assigned_machine_id = product.machine_id


@listens_for(Order, 'before_insert')
def before_order_insert(mapper, connection, target):
    calculate_order_details(target)    
    
  
@listens_for(Order, 'before_update')
def before_order_update(mapper, connection, target):
    calculate_order_details(target)


@listens_for(ProductionEntry, 'before_update')
def before_productionentry_update(mapper, connection, target):
    print "========== before production entry update ========="
    if target.num_hourly_good:
        num_good = sum([int(x) for x in target.num_hourly_good.split(',')])
        target.num_good = num_good
    
    if target.num_hourly_bad:
        num_bad = sum([int(x) for x in target.num_hourly_bad.split(',')])
        target.num_bad = num_bad


@listens_for(ProductionEntry, 'after_update')
def after_productionentry_update(mapper, connection, target):
    print "========== after production entry update ========="
    order = Order.query.get(target.order_id)
    if order.remaining <= 0:
        Order.query.filter_by(id=target.order_id).update({ 
            'status': 'COMPLETED', 
            'production_end_at': datetime.now() 
        })
 
        

    
import enum
from app import db


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

"""
class Product(Base):
# m-m
    colors = db.relationship(
        'Color',
        secondary=colors,
        backref=db.backref('products', lazy='dynamic')
    )
"""

class Product(Base):
    '''Model for product table'''
    __tablename__ = 'product'
    name = db.Column(db.String, nullable=False, unique=True)
    weight = db.Column(db.Integer, nullable=False)
    time_to_build = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer, nullable=False)
    mold_id = db.Column(db.Integer)
    photo = db.Column(db.String)
    # color_id = db.Column(db.Integer(), db.ForeignKey(Color.id))
    colors = db.relationship(Color, secondary=product_colors_table)
    # default_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))]
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    machine = db.relationship(Machine, backref='machine')

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class Order(Base):
    """Order table ORM mapping"""
    __tablename__ = 'order'
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('AUTO', 'PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SHIPPED'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(Product, backref='product')
    multi_colors_ratio = db.Column(db.String)
    raw_material_quantity = db.Column(db.Integer, nullable=False)
    is_raw_material_checkout = db.Column(db.Boolean, nullable=False, default=False)
    estimated_time_to_complete = db.Column(db.Integer)
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    assigned_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    # NOTE: backref name MUST be unique between relationships.
    assigned_machine = db.relationship(Machine, backref='order_to_machine')


    def __init__(self):
        self.is_raw_material_checkout = False


    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


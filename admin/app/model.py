import enum
from app import db


class StringPKBase(db.Model):
    """
    Define a base model with supports custom string primary key for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


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
    
    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            power_in_kilowatt=self.power_in_kilowatt,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return 'Machine xxxx'

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

"""
m-m mapping
colors = db.Table(
    'product_color',
    db.Model.metadata,
    db.Column('product_id', db.String, db.ForeignKey('product.id')),
    db.Column('color_id', db.String, db.ForeignKey('color.id'))
)
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
    name = db.Column(db.String)
    weight = db.Column(db.Integer)
    time_to_build = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer)
    mold_id = db.Column(db.Integer)
    default_machine_id = db.Column(db.Integer)
    photo_url = db.Column(db.String)
    color_id = db.Column(db.Integer(), db.ForeignKey(Color.id))
    color = db.relationship(Color, backref='colors')

    def __repr__(self):
        return '%d - %s' % (self.id, self.name )

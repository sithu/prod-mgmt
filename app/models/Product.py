from app import db
from datetime import datetime
from sqlalchemy import text
from RawMaterial import RawMaterial
from Base import Base
from StringPKBase import StringPKBase

colors = db.Table(
    'product_color',
    db.Column('product_id', db.String, db.ForeignKey('product.id')),
    db.Column('color_id', db.String, db.ForeignKey('color.id'))
)

class Product(StringPKBase):
    __tablename__ = 'product'
    name = db.Column(db.String)
    weight = db.Column(db.Integer)
    time_to_build = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer)
    mold_id = db.Column(db.Integer)
    # m-m
    colors = db.relationship(
        'Color',
        secondary=colors,
        backref=db.backref('products', lazy='dynamic')
    )

    def to_dict(self):
        """
        return a dict
        """
        return dict(
            id=self.id,
            name=self.name,
            type=self.type,
            weight=self.weight,
            time_to_build=self.time_to_build,
            selling_price=self.selling_price,
            colors=self.colors,
            num_employee_required=self.num_employee_required,
            created_at=str(self.created_at),
            updated_at=str(self.updated_at),
            mold_id=self.mold_id
        )

    def __repr__(self):
        return '<Product %r>' % (self.id)

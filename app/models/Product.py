from app import db
from datetime import datetime
from sqlalchemy import text
from RawMaterial import RawMaterial
from Base import Base

class Product(Base):
    __tablename__ = 'product'
    name = db.Column(db.String)
    weight = db.Column(db.Integer)
    time_to_build = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)
    color = db.Column(db.String)
    num_employee_required = db.Column(db.Integer)
    mold_id = db.Column(db.Integer)
    # 1-m
    raw_material_id = db.Column(db.ForeignKey('raw_material.id'))
    #rawmaterial = db.relationship(RawMaterial, backref='rawmaterials')

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
            color=self.color,
            num_employee_required=self.num_employee_required,
            created_at=str(self.created_at),
            updated_at=str(self.updated_at),
            mold_id=self.mold_id,
            raw_material_id=self.raw_material_id
        )

    def __repr__(self):
        return '<Product %r>' % (self.id)

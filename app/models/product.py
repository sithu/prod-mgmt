from app import db
from datetime import datetime
from sqlalchemy import text

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    type = db.Column(db.Enum('chair', 'stool', 'basket', 'cup', 'bowl'))
    
    weight = db.Column(db.Integer)
    
    time_to_build = db.Column(db.Integer)
    
    selling_price = db.Column(db.Integer)
    
    color = db.Column(db.Enum('white', 'red', 'green', 'blue', 'yellow', 'clear', 'grey', 'brown', 'other'))
    
    num_employee_required = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default=text("now()"))
    
    #updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now)
    updated_at = db.Column(db.DateTime, server_default=text("now()"), server_onupdate=text("now()"))
    
    # 1-m 
    raw_material_id = db.Column(db.Integer, db.ForeignKey('raw_material.id'))

    def to_dict(self):
        return dict(
            name = self.name,
            type = self.type,
            weight = self.weight,
            time_to_build = self.time_to_build,
            selling_price = self.selling_price,
            color = self.color,
            num_employee_required = self.num_employee_required,
            created_at = str(self.created_at),
            updated_at = str(self.updated_at),
            id = self.id,
            raw_material_id = self.raw_material_id
        )

    def __repr__(self):
        return '<Product %r>' % (self.id)

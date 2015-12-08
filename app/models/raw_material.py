from app import db
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import func

class Raw_material(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    weight = db.Column(db.Integer)
    
    count = db.Column(db.Integer)
    
    purchase_price = db.Column(db.Integer)
    
    color = db.Column(db.Enum('white', 'red', 'green', 'blue', 'yellow', 'clear', 'grey', 'brown', 'other'))
    
    created_at = db.Column(db.DateTime, server_default=func.now())
    
    updated_at = db.Column(db.DateTime, server_default=func.now(), server_onupdate=func.now())
    
    # 1-m relationship
    products = db.relationship('Product', backref='raw_material', lazy='dynamic')

    def to_dict(self):
        return dict(
            name = self.name,
            weight = self.weight,
            count = self.count,
            purchase_price = self.purchase_price,
            color = self.color,
            created_at = self.created_at,
            updated_at = self.updated_at,
            id = self.id
        #    products = self.products
        )

    def __repr__(self):
        return '<Raw_material %r>' % (self.id)

from app import db

class Raw_material(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    weight = db.Column(db.Integer)
    
    count = db.Column(db.Integer)
    
    purchase_price = db.Column(db.Integer)
    
    color = db.Column(db.Enum('white', 'red', 'green', 'blue', 'yellow', 'clear', 'grey', 'brown', 'other'))
    
    created_at = db.Column(db.Date)
    
    updated_at = db.Column(db.Date)
    

    def to_dict(self):
        return dict(
            name = self.name,
            weight = self.weight,
            count = self.count,
            purchase_price = self.purchase_price,
            color = self.color,
            created_at = self.created_at.isoformat(),
            updated_at = self.updated_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<Raw_material %r>' % (self.id)

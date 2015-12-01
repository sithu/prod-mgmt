from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    type = db.Column(db.Enum('chair', 'stool', 'basket', 'cup', 'bowl'))
    
    weight = db.Column(db.Integer)
    
    time_to_build = db.Column(db.Integer)
    
    selling_price = db.Column(db.Integer)
    
    color = db.Column(db.Enum('white', 'red', 'green', 'blue', 'yellow', 'clear', 'grey', 'brown', 'other'))
    
    created_at = db.Column(db.Date)
    
    updated_at = db.Column(db.Date)
    

    def to_dict(self):
        return dict(
            name = self.name,
            type = self.type,
            weight = self.weight,
            time_to_build = self.time_to_build,
            selling_price = self.selling_price,
            color = self.color,
            created_at = self.created_at.isoformat(),
            updated_at = self.updated_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<Product %r>' % (self.id)

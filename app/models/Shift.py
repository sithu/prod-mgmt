from app import db

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    shift_name = db.Column(db.String)
    
    start_time = db.Column(db.Integer)
    
    end_time = db.Column(db.Integer)
    

    def to_dict(self):
        return dict(
            shift_name = self.shift_name,
            start_time = self.start_time,
            end_time = self.end_time,
            id = self.id
        )

    def __repr__(self):
        return '<Shift %r>' % (self.id)

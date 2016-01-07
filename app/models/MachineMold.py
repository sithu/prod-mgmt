from app import db

class MachineMold(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    mold_type = db.Column(db.String)
    
    time_to_install = db.Column(db.Integer)
    
    created_at = db.Column(db.Date)
    
    modified_at = db.Column(db.Date)
    

    def to_dict(self):
        return dict(
            mold_type = self.mold_type,
            time_to_install = self.time_to_install,
            created_at = self.created_at.isoformat(),
            modified_at = self.modified_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<MachineMold %r>' % (self.id)

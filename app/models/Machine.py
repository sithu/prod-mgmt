from app import db

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    supported_mold_type = db.Column(db.Integer)
    
    installed_mold_id = db.Column(db.Integer)
    
    status = db.Column(db.String)
    
    downtime_start = db.Column(db.Date)
    
    downtime_end = db.Column(db.Date)
    
    total_downtime = db.Column(db.Integer)
    
    created_at = db.Column(db.Date)
    
    modified_at = db.Column(db.Date)
    

    def to_dict(self):
        return dict(
            name = self.name,
            supported_mold_type = self.supported_mold_type,
            installed_mold_id = self.installed_mold_id,
            status = self.status,
            downtime_start = self.downtime_start.isoformat(),
            downtime_end = self.downtime_end.isoformat(),
            total_downtime = self.total_downtime,
            created_at = self.created_at.isoformat(),
            modified_at = self.modified_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<Machine %r>' % (self.id)

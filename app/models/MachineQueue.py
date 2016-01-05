from app import db

class MachineQueue(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    machine_id = db.Column(db.Integer)
    
    work_in_progress = db.Column(db.String)
    
    slot_1 = db.Column(db.Integer)
    
    slot_2 = db.Column(db.Integer)
    
    slot_3 = db.Column(db.Integer)
    
    slot_4 = db.Column(db.Integer)
    
    slot_5 = db.Column(db.Integer)
    

    def to_dict(self):
        return dict(
            machine_id = self.machine_id,
            work_in_progress = self.work_in_progress,
            slot_1 = self.slot_1,
            slot_2 = self.slot_2,
            slot_3 = self.slot_3,
            slot_4 = self.slot_4,
            slot_5 = self.slot_5,
            id = self.id
        )

    def __repr__(self):
        return '<MachineQueue %r>' % (self.id)

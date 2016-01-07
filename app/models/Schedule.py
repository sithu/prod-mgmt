from app import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    date = db.Column(db.Date)
    
    shift_name = db.Column(db.String)
    
    employee_id = db.Column(db.Integer)
    
    manager_id = db.Column(db.Integer)
    
    is_in_duty = db.Column(db.Boolean)
    
    assigned_machine = db.Column(db.Integer)
    
    sign_in_at = db.Column(db.Date)
    
    sign_out_at = db.Column(db.Date)
    

    def to_dict(self):
        return dict(
            date = self.date.isoformat(),
            shift_name = self.shift_name,
            employee_id = self.employee_id,
            manager_id = self.manager_id,
            is_in_duty = self.is_in_duty,
            assigned_machine = self.assigned_machine,
            sign_in_at = self.sign_in_at.isoformat(),
            sign_out_at = self.sign_out_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<Schedule %r>' % (self.id)

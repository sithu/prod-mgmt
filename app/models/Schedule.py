from app import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    date = db.Column(db.Date)
    
    shift_name = db.Column(db.String)
    
    # user_id
    employee_id = db.Column(db.Integer)
    
    # user_id
    lead_id = db.Column(db.Integer)
    
    total_working_hours = db.Column(db.Integer)
    
    assigned_machine = db.Column(db.Integer)
    
    sign_in_at = db.Column(db.Date)
    
    sign_out_at = db.Column(db.Date)
    
    def to_dict(self):
        return dict(
            date = self.date.isoformat(),
            shift_name = self.shift_name,
            employee_id = self.employee_id,
            manager_id = self.manager_id,
            total_working_hours = self.total_working_hours,
            assigned_machine = self.assigned_machine,
            sign_in_at = self.sign_in_at.isoformat(),
            sign_out_at = self.sign_out_at.isoformat(),
            id = self.id
        )

    def __repr__(self):
        return '<Schedule %r>' % (self.id)

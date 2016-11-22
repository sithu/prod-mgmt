from app import db

class ProductionEntry(db.Model):
    __tablename__ = 'production_entry'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    status = db.Column(db.Enum('PLANNED', ' IN_PROGRESS', ' COMPLETED', ' SHIPPED'))

    shift_name = db.Column(db.String)

    machine_id = db.Column(db.Integer)

    raw_material_id = db.Column(db.Integer)

    order_id = db.Column(db.Integer)

    team_lead_id = db.Column(db.Integer)

    team_lead_name = db.Column(db.String)

    estimated_time_to_finish = db.Column(db.Integer)

    start = db.Column(db.Date)

    end = db.Column(db.Date)

    delay = db.Column(db.Integer)

    delay_reason = db.Column(db.String)

    planned_quantity = db.Column(db.Integer)

    finished_quantity = db.Column(db.Integer)

    defected_quantity = db.Column(db.Integer)


    def to_dict(self):
        return dict(
            status = self.status,
            shift_name = self.shift_name,
            machine_id = self.machine_id,
            raw_material_id = self.raw_material_id,
            order_id = self.order_id,
            team_lead_id = self.team_lead_id,
            team_lead_name = self.team_lead_name,
            estimated_time_to_finish = self.estimated_time_to_finish,
            start = self.start.isoformat(),
            end = self.end.isoformat(),
            delay = self.delay,
            delay_reason = self.delay_reason,
            planned_quantity = self.planned_quantity,
            finished_quantity = self.finished_quantity,
            defected_quantity = self.defected_quantity,
            id = self.id
        )

    def __repr__(self):
        return '<ProductionEntry %r>' % (self.id)

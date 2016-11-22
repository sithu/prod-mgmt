from app import db


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    status = db.Column(db.Enum('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SHIPPED'))

    product_id = db.Column(db.Integer)

    quantity = db.Column(db.Integer)

    raw_material_quantity = db.Column(db.Integer)

    created_at = db.Column(db.Date)

    estimated_time_to_finish = db.Column(db.Integer)

    production_start_at = db.Column(db.Date)

    production_end_at = db.Column(db.Date)

    note = db.Column(db.String)

    # 1-1 
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            status=self.status,
            product_id=self.product_id,
            quantity=self.quantity,
            raw_material_quantity=self.raw_material_quantity,
            created_at=self.created_at.isoformat(),
            estimated_time_to_finish=self.estimated_time_to_finish,
            production_start_at=self.production_start_at.isoformat(),
            production_end_at=self.production_end_at.isoformat(),
            machine_id=self.machine_id,
            note=self.note,
        )

    def __repr__(self):
        return '<Order %r>' % (self.id)

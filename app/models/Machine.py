from app import db
from app.models.StringPKBase import StringPKBase

class Machine(StringPKBase):
    __tablename__ = 'machine'

    name = db.Column(db.String, nullable=False, unique=True)

    status = db.Column(db.String, default='Available')

    ''' 1-1 relationship
    order = db.relationship(
        'Order',
        backref='machine',
        uselist=False
    )
    '''

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '<Machine %r>' % (self.id)

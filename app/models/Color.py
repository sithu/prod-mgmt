from app import db
from app.models.Base import Base

class Color(Base):
    __tablename__ = 'color'
    name = db.Column(db.String)
    
    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '<Color %r>' % (self.id)

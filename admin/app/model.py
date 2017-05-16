from app import db

class StringPKBase(db.Model):
    """
    Define a base model with supports custom string primary key for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Base(db.Model):
    """
    Define a base model for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Color(StringPKBase):
    """
    class doc
    """
    __tablename__ = 'color'
    name = db.Column(db.String, nullable=False, unique=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '<Color %r>' % (self.id)
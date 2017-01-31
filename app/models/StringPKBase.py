from app import db

class StringPKBase(db.Model):
    """
    Define a base model with supports custom string primary key for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
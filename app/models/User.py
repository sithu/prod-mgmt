from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    email = db.Column(db.String)
    
    password_hash = db.Column(db.String)
    
    # TODO: role_id

    def to_dict(self):
        return dict(
            name = self.name,
            email = self.email,
            id = self.id
        )

    def __repr__(self):
        return '<User %r>' % (self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password_plain):
        self.password_hash = generate_password_hash(password_plain)
    
    def verify_password(self, password_plain):
        return check_password_hash(self.password_hash, password_plain)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

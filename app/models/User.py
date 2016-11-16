from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)

    email = db.Column(db.String)

    phone = db.Column(db.String)

    password_hash = db.Column(db.String)

    level = db.Column(db.Integer)

    salary = db.Column(db.Integer)

    department = db.Column(db.String)

    status = db.Column(db.Enum('IN', 'OUT', 'SICK','VACATION'))

    shift_name = db.Column(db.Enum('Morning', 'Evening', 'Night'))

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    profile_photo_url = db.Column(db.String)

    last_login_at = db.Column(db.Date)

    modified_at = db.Column(db.Date)

    gender =  db.Column(db.Enum('M','F'))

    def to_dict(self):
        dict = {
                    'name': self.name, 
                    'email': self.email, 
                    'phone': self.phone, 
                    'gender': self.gender,
                    'level': self.level, 
                    'salary': self.salary,
                    'department': self.department, 
                    'status': self.status, 
                    'shift_name': self.shift_name,
                    'id': self.id,
                    'profile_photo_url': self.profile_photo_url
                }

        if self.start_date is not None:
            dict['start_date'] = self.start_date.isoformat()

        if self.end_date is not None:
            dict['end_date'] = self.end_date.isoformat()

        if self.last_login_at is not None:
            dict['last_login_at'] = self.last_login_at.isoformat()

        if self.modified_at is not None:
            dict['modified_at'] = self.modified_at.isoformat()

        return dict

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

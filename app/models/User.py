from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    email = db.Column(db.String)
    
    phone = db.Column(db.String)

    password_hash = db.Column(db.String)
    
    level = db.Column(db.Integer)

    salary = db.Column(db.Integer)

    department = db.Column(db.String)

    # in, late, on_vacation, on_holiday
    status = db.Column(db.String)

    shift_name = db.Column(db.String)

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    profile_photo_url = db.Column(db.String)

    # format: "YYYY-MM-DD HH:MM:SS"
    modified_at = db.Column(db.String)

    last_login_at = db.Column(db.String)

    # TODO: role_id

    def to_dict(self):
        return dict(
            name = self.name,
            email = self.email,
            phone = self.phone,
            level = self.level,
            salary = self.salary,
            department = self.department,
            status = self.status,
            shift_name = self.shift_name,
            start_date = self.start_date,
            end_date = self.end_date,
            profile_photo_url = self.profile_photo_url,
            modified_at = self.modified_at,
            last_login_at = self.last_login_at,
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

import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from app.models.User import User
from app.models.Order import Order
from app.models.Machine import Machine
from datetime import datetime

app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)
migrate = Migrate(app, db)

# migrations
manager.add_command('db', MigrateCommand)

SHIFTS = [ 'Morning', 'Evening', 'Night' ]

@manager.command
def hello():
    print "hello"

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Order=Order, Machine=Machine)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    print "creating admin user..."
    db.session.add(User(name='Administrator', email='cedar-admin@gmail.com', password='admin', level=0))
    db.session.commit()


@manager.command
def create_managers():
    """Creates a set of supervisors."""
    for i in range(0, 3):
        _name = 'Manager %d' % i
        _email = 'cedar-manager-%d@gmail.com' % i
        print "creating a manager account...", _email
        user = User(
            name=_name, 
            email=_email, 
            password='manager', 
            department='Production', 
            shift_name=SHIFTS[i % 3],
            level=3,
            status='AVAILABLE',
            gender='M',
            start_date=datetime.now(),
            salary=100000
            )
        print "new manager=", user.name, user.shift_name
        db.session.add(user)
    
    db.session.commit()


@manager.command
def create_supervisors():
    """Creates a set of supervisors."""
    for i in range(0, 10):
        _name = 'Supervisor %d' % i
        _email = 'cedar-sup-%d@gmail.com' % i
        print "creating a supervisor account...", _email
        user = User(
            name=_name, 
            email=_email, 
            password='sup', 
            department='Production', 
            shift_name=SHIFTS[i % 3],
            level=4,
            status='AVAILABLE',
            gender='M',
            start_date=datetime.now(),
            salary=50000
            )
        print "new user=", user.name, user.shift_name
        db.session.add(user)
    
    db.session.commit()

@manager.command
def create_workers():
    """Creates a set of supervisors."""
    for i in range(0, 40):
        _name = 'Worker %d' % i
        _email = 'cedar-worker-%d@gmail.com' % i
        print "creating a worker account...", _email
        user = User(
            name=_name, 
            email=_email, 
            password='worker', 
            department='Production', 
            shift_name=SHIFTS[i % 3],
            level=5,
            status='AVAILABLE',
            gender='M',
            start_date=datetime.now(),
            salary=20000
            )
        db.session.add(user)
    
    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    pass


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
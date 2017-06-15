import datetime
from app import app, db
from app.model import Color, Machine, Product, Shift

def build_sample_db():
    db.drop_all()
    db.create_all()
    print "Creating test data..."
    create_colors()
    create_machines()
    create_shift()
    db.session.commit()


def create_colors():
    print "Creating Color..."
    color_names = [
        'White', 'Green', 'Blue', 'Red'
    ]
    color_codes = [
        '#100', '#101', '#102', '#103'
    ]

    for i in range(len(color_names)):
        color = Color()
        color.color_code = color_codes[i]
        color.name = color_names[i]
        db.session.add(color)

def create_machines():
    print "Creating Machine..."
    names = [ 'Machine A', 'Machine B', 'Machine C', 'Machine D' ]
    kw = [ 1000, 1500, 2000, 2500 ]

    for i in range(len(names)):
        m = Machine()
        m.name = names[i]
        m.status = 'OFF'
        m.power_in_kilowatt = kw[i]
        db.session.add(m)

def create_shift():
    print "creating Shifts..."
    shifts = [ ('Morning', 8, 16), ('Evening', 16, 24), ('Night', 24, 8)]
    for t in shifts:
        s = Shift()
        s.shift_name = t[0]
        s.start_hour = t[1]
        s.end_hour = t[2]
        db.session.add(s)



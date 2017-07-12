import enum
import random
import calendar

from app import db
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property, scoped_session, sessionmaker, sessionmaker
from sqlalchemy import select, func, and_, event, UniqueConstraint
from datetime import datetime, date, timedelta
from sqlalchemy_utils import ColorType
from flask_security import UserMixin, RoleMixin
from flask import flash
from flask_admin.babel import gettext
from sqlalchemy.sql.expression import true
from util import slot_lead_to_machine

########################### Flask Security Models ######################
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# m-m User-to-ProductionEntry mapping for assembler role only
users_production_entries_table = db.Table(
    'users_production_entries',
    Column('user_id', Integer, db.ForeignKey('user.id')),
    Column('production_entry_id', Integer, db.ForeignKey('production_entry.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), nullable=False)
    phone = Column(String(15))
    gender = db.Column(db.Enum('M', 'F'), default='M', nullable=False)
    NFC_tag_id = db.Column(db.String(25))
    active = db.Column(db.Boolean(), default=True)
    is_in = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    photo = db.Column(db.String)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    shift = db.relationship('Shift', backref=db.backref('user_shift', lazy='dynamic'))

    def __str__(self):
        return self.name


############################ Cedar Models ##########################    
class Base(db.Model):
    """
    Define a base model for other database tables to inherit
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

########################## Models ################################
class Machine(Base):
    __tablename__ = 'machine'
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    status = db.Column(db.Enum('OFF', 'ON', 'BROKEN', 'NOT_IN_USE'), default='ON', nullable=False, index=True)
    power_in_kilowatt = db.Column(db.Integer) 
    photo = db.Column(db.String)
    average_num_workers = Column(db.Enum('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), default='1')
    machine_to_lead_ratio = db.Column(db.Enum('1-1', '1-2', '1-3', '1-4', '1-5'), default='1-1', nullable=False)
    
    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            power_in_kilowatt=self.power_in_kilowatt,
            photo=self.photo,
            average_num_workers=self.average_num_workers,
            machine_to_lead_ratio=self.machine_to_lead_ratio,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class Shift(db.Model):
    __tablename__ = 'shift'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)
    total_hours = Column(Integer, nullable=False)

    def __repr__(self):
        return '%s' % (self.name)

    def toAM_PM(self, hour):
        if hour == 12:
            return "12P.M"
        elif hour > 12:
            return "%dP.M" % (hour-12)
        else:
            return "%dA.M" % (hour)


class Color(db.Model):
    """
    class doc
    """
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.String, nullable=False, unique=True)
    color_code = Column(ColorType, nullable=False, unique=True)

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)

#m-m mapping
product_colors_table = db.Table(
    'product_color',
    db.Model.metadata,
    db.Column('product_id', db.String, db.ForeignKey('product.id')),
    db.Column('color_id', db.String, db.ForeignKey('color.id'))
)


class Product(Base):
    '''Model for product table'''
    __tablename__ = 'product'
    name = db.Column(db.String, nullable=False, unique=True)
    weight = db.Column(db.Integer, nullable=False)
    time_to_build = db.Column(db.Integer, nullable=False)
    selling_price = db.Column(db.Integer)
    num_employee_required = db.Column(db.Integer, nullable=False)
    raw_material_weight_per_bag = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String)
    multi_colors_ratio = db.Column(db.String)
    colors = db.relationship(Color, secondary=product_colors_table)
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id), nullable=False)
    machine = db.relationship(Machine, backref='machine')

    def __repr__(self):
        return '%d - %s' % (self.id, self.name)


class ProductionEntry(db.Model):
    __tablename__ = 'production_entry'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    shift_id = db.Column(db.Integer, db.ForeignKey(Shift.id), nullable=False)
    shift = db.relationship(Shift, backref='production_entry_shift')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref='production_entry_orders')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lead = db.relationship(User)
    num_hourly_good = db.Column(db.String, default='')
    num_hourly_bad = db.Column(db.String, default='')
    num_good = db.Column(db.Integer, default=0)
    num_bad = db.Column(db.Integer, default=0)
    date = Column(Date, default=date.today())
    members = db.relationship(User, secondary=users_production_entries_table)
    
    @hybrid_property
    def machine_id(self):
        return self.order.assigned_machine_id
    
    @hybrid_property
    def photo(self):
        return self.order.photo

    @hybrid_property
    def product_colors(self):
        return self.order.product_colors

    @hybrid_property
    def status(self):
        return self.order.status

    @hybrid_property
    def remaining(self):
        return self.order.remaining

    def save(self, *args, **kwargs):
        print "FIXME: override save method"
        # self.order.production_entries.append(self)
        # return super(ProductionEntry, self).save(*args, **kwargs)


class Order(db.Model):
    """Order table ORM mapping"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('NEW', 'IN_PROGRESS', 'COMPLETED'), nullable=False, default='NEW')
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, backref='product')
    raw_material_quantity = db.Column(db.Integer, nullable=False, default=0)
    estimated_time_to_complete = db.Column(db.Integer, nullable=False)
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    assigned_machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    # NOTE: backref name MUST be unique between relationships.
    assigned_machine = db.relationship(Machine, backref=db.backref('order_to_machine'))
    completed = column_property(
        select([func.sum(ProductionEntry.num_good)]).\
            where(ProductionEntry.order_id==id).\
            correlate_except(ProductionEntry)
    )

    def __repr__(self):
        return '%d - %s - %s' % (self.id, self.name, self.status)

    @hybrid_property
    def photo(self):
        return self.product.photo

    @hybrid_property
    def product_colors(self):
        return self.product.colors

    @hybrid_property
    def remaining(self):
        return self.quantity - self.completed


class TeamRequest(Base):
    __tablename__ = 'team_request'
    start_date = db.Column(db.Date, default=(date.today() + timedelta(days=1)), nullable=False)
    end_date = db.Column(db.Date, default=(date.today() + timedelta(days=1)), nullable=False)
    day_off = db.Column(db.String(25))
    
    def __repr__(self):
        return '%s - %s' % (self.start_date, self.end_date)


# m-m User-to-Team mapping
user_team_table = db.Table(
    'user_team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

user_team_standbys_table = db.Table(
    'user_team_standbys',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

class Team(Base):
    __tablename__ = 'team'
    date = Column(Date, default=date.today(), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    shift = db.relationship(Shift, backref=db.backref('team_shift', lazy='dynamic'))
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id), nullable=False)
    machine = db.relationship(Machine, backref=db.backref('team_machine', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lead = db.relationship(User)
    members = db.relationship(User, secondary=user_team_table)
    standbys = db.relationship(User, secondary=user_team_standbys_table)
    #__table_args__ = (UniqueConstraint('date', 'shift_id', 'machine_id', name='_date_shift_machine_uc'),)
    
    def __repr__(self):
        return '%d - %s - %s' % (self.id, self.shift.name, self.date)

    @hybrid_property
    def member_size(self):
        if self.members:
            return len(self.members)
        else:
            return 0

    @hybrid_property
    def week_day(self):
        if self.date:
            return calendar.day_name[self.date.weekday()]
        else:
            return ''


############ ORM Triggers #############
from sqlalchemy.event import listens_for
from decimal import *

def calculate_order_details(target):
    # 1. Calculate number of raw material bags.
    product = Product.query.get(target.product_id)
    weight = Decimal(product.weight)
    total_weight = Decimal(target.quantity) * weight
    num_raw_bag = Decimal(total_weight) / product.raw_material_weight_per_bag
    # round results to fixed number
    target.raw_material_quantity = int(Decimal(num_raw_bag).quantize(Decimal('1.'), rounding=ROUND_UP))
    
    # 2. Calculate estimated time to complete
    target.estimated_time_to_complete = target.quantity * product.time_to_build

    # 3. Set the mode based on the machine id is default or not.
    if not target.assigned_machine_id:
        target.assigned_machine_id = product.machine_id


@listens_for(Order, 'before_insert')
def before_order_insert(mapper, connection, target):
    calculate_order_details(target)    
    
  
@listens_for(Order, 'before_update')
def before_order_update(mapper, connection, target):
    calculate_order_details(target)


@listens_for(ProductionEntry, 'before_update')
def before_productionentry_update(mapper, connection, target):
    print "========== before production entry update ========="
    if target.num_hourly_good:
        num_good = sum([int(x) for x in target.num_hourly_good.split(',')])
        target.num_good = num_good
    
    if target.num_hourly_bad:
        num_bad = sum([int(x) for x in target.num_hourly_bad.split(',')])
        target.num_bad = num_bad


@listens_for(ProductionEntry, 'after_update')
def after_productionentry_update(mapper, connection, target):
    print "========== after production entry update ========="
    order = Order.query.get(target.order_id)
    if order.remaining <= 0:
        Order.query.filter_by(id=target.order_id).update({ 
            'status': 'COMPLETED', 
            'production_end_at': datetime.now() 
        })
 

@listens_for(TeamRequest, 'after_insert')
def after_teamrequest_insert(mapper, connection, target):     
    print "============ after team reqeust insert =============="
    print target.day_off, target.start_date, target.end_date
    txn = connection.begin()
    Session = sessionmaker()
    session = Session(bind=connection)
    teams = []
    try:
        machines = session.query(Machine).filter(Machine.status != 'NOT_IN_USE').all()
        assemblers = session.query(User).filter(and_(User.active == true(), User.roles.any(name='assembler'))).all()
        random.shuffle(assemblers)
        leads = session.query(User).filter(and_(User.active == true(), User.roles.any(name='lead'))).all()
        random.shuffle(leads)
        shifts = session.query(Shift).all()
        assembler_map = {}
        for s in shifts:
            assembler_map[s.id] = []
        while assemblers:
            a = assemblers.pop()
            assembler_map[a.shift_id].append(a)
        
        lead_slot, extra = slot_lead_to_machine(leads, machines)
        if len(lead_slot) != len(machines):
            print "Total lead slot does not match with number of machines."
            return
        teams = from_start_to_end_date(target.start_date, target.end_date, target.day_off, shifts, machines, assembler_map, lead_slot, extra)
        if len(teams) > 0:
            session.add_all(teams)
            session.commit()
        txn.commit()
    except Exception as ex:
        txn.rollback()
        flash(gettext('Failed to create teams. %(error)s', error=str(ex)), 'error')
        print ex

    finally:
        txn.close()



def from_start_to_end_date(start, end, day_off_str, shifts, machines, assembler_map, leader_slot, extra):
    day_offs = []
    if day_off_str and len(day_off_str.strip()) > 0:
        day_offs = [ int(x) for x in day_off_str.split(',') ]
    teams = []
    while start <= end:
        # check current date is in the day offs list
        if start.weekday() in day_offs:
            start += timedelta(days=1) 
            continue

        for s in shifts:
            m_copy = machines[:]
            leaders = leader_slot[:]
            m = m_copy.pop()
            l = leaders.pop()
            members = []
            standbys = []
            for a in assembler_map[s.id]:
                if len(members) < int(m.average_num_workers):
                    members.append(a)
                elif len(m_copy) > 0:
                    # Save a team to DB.
                    t = Team(date=start, shift_id=s.id, machine_id=m.id, user_id=l.id, members=members, standbys=[])
                    teams.append(t)
                    m = m_copy.pop()
                    l = leaders.pop()
                    members = [a]
                else:
                    standbys.append(a)
            
            if len(standbys) > 0 or len(members) > 0:
                # Save the last team with standbys 
                print "saving standbys = %d, last mem = %d" % (len(standbys),  len(members))
                standbys.extend(extra)
                t = Team(date=start, shift_id=s.id, machine_id=m.id, user_id=l.id, members=members, standbys=standbys)
                teams.append(t)
            
        start += timedelta(days=1) 
        # end of while loop
    
    return teams
            
############################# Histroy Models ##########################
class OrderHistory(db.Model):
    """Order table ORM mapping"""
    __tablename__ = 'order_history'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    product_id = db.Column(db.Integer, index=True)
    product_name = Column(String(75), index=True)
    raw_material_quantity = db.Column(db.Integer, nullable=False, default=0)
    estimated_time_to_complete = db.Column(db.Integer, nullable=False)
    machine_id = Column(Integer, index=True)
    machine_name = Column(String, index=True)
    photo = Column(String(100))
    order_created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    production_start_at = db.Column(db.DateTime)
    production_end_at = db.Column(db.DateTime)
    note = db.Column(db.String)
    
    def __repr__(self):
        return '%d - %s - %s' % (self.id, self.name, self.product_name)


class ProductionEntryHistory(db.Model):
    __tablename__ = 'production_entry_history'
    id = Column(Integer, primary_key = True, index=True)
    date = Column(Date, default=date.today())
    shift_name = Column(String(50), index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_history.id'), nullable=False)
    order = db.relationship('OrderHistory', backref='production_entry_h_order_h')
    lead = Column(String, index=True)
    assemblers = Column(String)
    num_hourly_good = Column(String, default='')
    num_hourly_bad = Column(String, default='')
    num_good = Column(Integer, default=0)
    num_bad = Column(Integer, default=0)
    machine_id = Column(Integer, index=True)
    photo = Column(String(100))
    
    def __repr__(self):
        return '%d - %d - %s' % (self.id, self.order_id, self.shift_name)


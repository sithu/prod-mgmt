from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
machine = Table('machine', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('supported_mold_type', Integer),
    Column('installed_mold_id', Integer),
    Column('status', String),
    Column('downtime_start', Date),
    Column('downtime_end', Date),
    Column('total_downtime', Integer),
    Column('created_at', Date),
    Column('modified_at', Date),
)

machine_mold = Table('machine_mold', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('mold_type', String),
    Column('time_to_install', Integer),
    Column('created_at', Date),
    Column('modified_at', Date),
)

machine_queue = Table('machine_queue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('machine_id', Integer),
    Column('work_in_progress', String),
    Column('slot_1', Integer),
    Column('slot_2', Integer),
    Column('slot_3', Integer),
    Column('slot_4', Integer),
    Column('slot_5', Integer),
)

schedule = Table('schedule', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', Date),
    Column('shift_name', String),
    Column('employee_id', Integer),
    Column('manager_id', Integer),
    Column('is_in_duty', Boolean),
    Column('assigned_machine', Integer),
    Column('sign_in_at', Date),
    Column('sign_out_at', Date),
)

shift = Table('shift', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('shift_name', String),
    Column('start_time', Integer),
    Column('end_time', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['machine'].create()
    post_meta.tables['machine_mold'].create()
    post_meta.tables['machine_queue'].create()
    post_meta.tables['schedule'].create()
    post_meta.tables['shift'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['machine'].drop()
    post_meta.tables['machine_mold'].drop()
    post_meta.tables['machine_queue'].drop()
    post_meta.tables['schedule'].drop()
    post_meta.tables['shift'].drop()

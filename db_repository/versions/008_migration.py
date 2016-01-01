from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
production_entry = Table('production_entry', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('status', String),
    Column('shift_name', String),
    Column('machine_id', Integer),
    Column('raw_material_id', Integer),
    Column('order_id', Integer),
    Column('team_lead_id', Integer),
    Column('team_lead_name', String),
    Column('estimated_time_to_finish', Integer),
    Column('start', Date),
    Column('end', Date),
    Column('delay', Integer),
    Column('delay_reason', String),
    Column('planned_quantity', Integer),
    Column('finished_quantity', Integer),
    Column('defected_quantity', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['production_entry'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['production_entry'].drop()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('status', Enum('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'SHIPPED')),
    Column('product_id', Integer),
    Column('quantity', Integer),
    Column('raw_material_quantity', Integer),
    Column('created_at', Date),
    Column('estimated_time_to_finish', Integer),
    Column('production_start_at', Date),
    Column('production_end_at', Date),
    Column('note', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].drop()

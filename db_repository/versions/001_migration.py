from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('type', Enum('chair', 'stool', 'basket', 'cup', 'bowl')),
    Column('weight', Integer),
    Column('time_to_build', Integer),
    Column('selling_price', Integer),
    Column('color', Enum('white', 'red', 'green', 'blue', 'yellow', 'clear', 'grey', 'brown', 'other')),
    Column('created_at', Date),
    Column('updated_at', Date),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].drop()

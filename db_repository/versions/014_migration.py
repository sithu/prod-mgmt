from sqlalchemy import *
from migrate import *

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('product', meta, autoload=True)
    col = Column('mold_id', Integer)
	col.create(table, populate_default=True)
		

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('product', meta, autoload=True)
    table.c.mold_id.drop()
	

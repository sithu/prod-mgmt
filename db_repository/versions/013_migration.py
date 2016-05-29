from sqlalchemy import *
from migrate import *

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('machine', meta, autoload=True)
    col = Column('supervisor_attention', Integer)
	col.create(table, populate_default=True)
	col = Column('num_worker_needed', Integer, default=2)
    col.create(table, populate_default=True)
		

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    table = Table('machine', meta, autoload=True)
    table.c.supervisor_attention.drop()
	table.c.num_worker_needed.drop()


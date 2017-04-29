"""empty message

Revision ID: 70f7e713729f
Revises: 589d846f900c
Create Date: 2017-03-19 23:32:05.248356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70f7e713729f'
down_revision = '589d846f900c'
branch_labels = None
depends_on = None


def upgrade():
    print "creating product table..."
    op.create_table(
        'product',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.current_timestamp()),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False),
        sa.Column('time_to_build', sa.Integer(), nullable=False),
        sa.Column('selling_price', sa.Integer(), nullable=True),
        sa.Column('num_employee_required', sa.Integer(), nullable=True),
        sa.Column('mold_id', sa.Integer(), nullable=True),
        sa.Column('photo_url', sa.String()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    print "creating product_color table..."
    op.create_table(
        'product_color',
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('color_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['color_id'], ['color.id']),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'])
    )
    ### end Alembic commands ###


def downgrade():
    op.drop_table('product_color')
    op.drop_table('product')

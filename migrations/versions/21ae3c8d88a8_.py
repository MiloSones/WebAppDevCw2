"""empty message

Revision ID: 21ae3c8d88a8
Revises: b95d3d8c7291
Create Date: 2024-12-04 03:50:13.996433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ae3c8d88a8'
down_revision = 'b95d3d8c7291'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock', sa.Integer(), nullable=False, server_default='0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('stock')

    # ### end Alembic commands ###

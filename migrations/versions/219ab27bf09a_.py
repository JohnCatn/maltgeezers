"""empty message

Revision ID: 219ab27bf09a
Revises: 1b7eed677875
Create Date: 2018-07-13 13:17:29.272565

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '219ab27bf09a'
down_revision = '1b7eed677875'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###
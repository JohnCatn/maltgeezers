"""empty message

Revision ID: c528693c8962
Revises: f606899c4c93
Create Date: 2018-07-12 20:53:20.399213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c528693c8962'
down_revision = 'f606899c4c93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendees',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('tasting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tasting_id'], ['tasting.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('user_tasting')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tasting',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('tasting_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['tasting_id'], ['tasting.id'], name='user_tasting_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_tasting_ibfk_2'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('attendees')
    # ### end Alembic commands ###

"""empty message

Revision ID: f606899c4c93
Revises: fb361e1bca33
Create Date: 2018-07-12 20:42:24.187138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f606899c4c93'
down_revision = 'fb361e1bca33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_tasting_ibfk_1', 'user_tasting', type_='foreignkey')
    op.drop_constraint('user_tasting_ibfk_2', 'user_tasting', type_='foreignkey')
    op.create_foreign_key(None, 'user_tasting', 'tasting', ['tasting_id'], ['id'])
    op.create_foreign_key(None, 'user_tasting', 'user', ['user_id'], ['id'])
    op.drop_column('user_tasting', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_tasting', sa.Column('id', mysql.INTEGER(display_width=11), nullable=False))
    op.drop_constraint(None, 'user_tasting', type_='foreignkey')
    op.drop_constraint(None, 'user_tasting', type_='foreignkey')
    op.create_foreign_key('user_tasting_ibfk_2', 'user_tasting', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('user_tasting_ibfk_1', 'user_tasting', 'tasting', ['tasting_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###

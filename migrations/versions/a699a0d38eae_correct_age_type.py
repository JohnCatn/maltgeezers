"""correct age type

Revision ID: a699a0d38eae
Revises: 82e80be3224c
Create Date: 2018-06-03 14:39:15.320178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a699a0d38eae'
down_revision = '82e80be3224c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('bottle_ibfk_1', 'bottle', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('bottle_ibfk_1', 'bottle', 'type', ['age'], ['id'])
    # ### end Alembic commands ###

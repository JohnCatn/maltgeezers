"""empty message

Revision ID: 8ae4bb3e7c30
Revises: 2f88b6f0ed23
Create Date: 2018-06-23 10:23:26.318847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ae4bb3e7c30'
down_revision = '2f88b6f0ed23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('postcode', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('postcode')
    )
    op.create_table('user_club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['club_id'], ['club.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('tasting', sa.Column('club_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasting', 'user', ['club_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasting', type_='foreignkey')
    op.drop_column('tasting', 'club_id')
    op.drop_table('user_club')
    op.drop_table('club')
    # ### end Alembic commands ###

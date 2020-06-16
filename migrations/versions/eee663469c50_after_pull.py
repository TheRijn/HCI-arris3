"""after pull

Revision ID: eee663469c50
Revises: 554ab1b72a09
Create Date: 2020-06-15 17:45:58.986349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee663469c50'
down_revision = '554ab1b72a09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('points', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'points')
    # ### end Alembic commands ###

"""ammount and timestamp

Revision ID: 8ff23e3a5165
Revises: 58ec177472fd
Create Date: 2020-06-16 15:55:10.033936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ff23e3a5165'
down_revision = '58ec177472fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise_log', sa.Column('amount', sa.Integer(), nullable=True))
    op.add_column('exercise_log', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('food_log', sa.Column('grams', sa.Integer(), nullable=True))
    op.add_column('food_log', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('food_log', 'timestamp')
    op.drop_column('food_log', 'grams')
    op.drop_column('exercise_log', 'timestamp')
    op.drop_column('exercise_log', 'amount')
    # ### end Alembic commands ###

"""add unique property to instruction.model

Revision ID: 08f6351e240a
Revises: db17afe6f7d9
Create Date: 2024-04-28 23:12:12.810736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08f6351e240a'
down_revision = 'db17afe6f7d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Instruction', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['order'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Instruction', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
"""fixing instruction model

Revision ID: 4739a29c3bba
Revises: 3e3a75742811
Create Date: 2024-04-24 20:23:13.498793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4739a29c3bba'
down_revision = '3e3a75742811'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Instruction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('instruction', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['order'])
        batch_op.drop_column('ingredient')
        batch_op.drop_column('step')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Instruction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('step', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('ingredient', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('instruction')
        batch_op.drop_column('order')

    # ### end Alembic commands ###
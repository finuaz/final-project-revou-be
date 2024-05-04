"""dropping instruction

Revision ID: 33917f6c9eef
Revises: 08f6351e240a
Create Date: 2024-04-29 23:33:43.618722

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '33917f6c9eef'
down_revision = '08f6351e240a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Instruction')
    with op.batch_alter_table('Recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instruction', sa.Text(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Recipe', schema=None) as batch_op:
        batch_op.drop_column('instruction')

    op.create_table('Instruction',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Instruction_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('instruction', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['User.id'], name='Instruction_author_id_fkey'),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], name='Instruction_recipe_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Instruction_pkey'),
    sa.UniqueConstraint('order', name='Instruction_order_key')
    )
    # ### end Alembic commands ###
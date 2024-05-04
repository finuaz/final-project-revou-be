"""re-rer-erer-er-er-er-er-er-erre-reinitialize

Revision ID: 17812e61ec72
Revises: 
Create Date: 2024-05-04 20:41:43.211141

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '17812e61ec72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category')
    )
    op.create_table('Ingredient',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ingredient', sa.String(length=40), nullable=False),
    sa.Column('ingredient_image', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Origin',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('origin', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('origin')
    )
    op.create_table('Tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tagname', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tagname')
    )
    op.create_table('Type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('new_password', sa.String(length=255), nullable=True),
    sa.Column('reset_password_question', sa.String(length=255), nullable=True),
    sa.Column('reset_password_answer', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('role', sa.Enum('USER', 'ADMIN', 'CHEF', 'EXPERT', name='userrole'), nullable=False),
    sa.Column('bio', sa.String(length=300), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('location', sa.String(length=30), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Following',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Recipe',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('nutriscore', sa.Integer(), nullable=True),
    sa.Column('cooktime', sa.Integer(), nullable=False),
    sa.Column('complexity', sa.String(length=20), nullable=False),
    sa.Column('servings', sa.Integer(), nullable=False),
    sa.Column('budget', sa.String(length=20), nullable=False),
    sa.Column('instruction', sa.Text(), nullable=False),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('Socials',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('facebook', sa.String(length=255), nullable=True),
    sa.Column('instagram', sa.String(length=255), nullable=True),
    sa.Column('tiktok', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Attachment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('attachment_link', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Like',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Nutrition',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('serving_per_container', sa.Integer(), nullable=True),
    sa.Column('serving_size', sa.String(length=20), nullable=True),
    sa.Column('calories', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_fat', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_carbohydrate', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('total_sugar', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('cholesterol', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('protein', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('vitamin_d', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('sodium', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('calcium', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('potassium', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('iron', sa.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Rate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Recipe_category',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['Category.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'category_id')
    )
    op.create_table('Recipe_ingredient',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['ingredient_id'], ['Ingredient.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'ingredient_id')
    )
    op.create_table('Recipe_origin',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('origin_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['origin_id'], ['Origin.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'origin_id')
    )
    op.create_table('Recipe_tag',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['Tag.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'tag_id')
    )
    op.create_table('Recipe_type',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['Recipe.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['Type.id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'type_id')
    )
    op.drop_table('wrappers_fdw_stats')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wrappers_fdw_stats',
    sa.Column('fdw_name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('create_times', sa.BIGINT(), autoincrement=False, nullable=True, comment='Total number of times the FDW instacne has been created'),
    sa.Column('rows_in', sa.BIGINT(), autoincrement=False, nullable=True, comment='Total rows input from origin'),
    sa.Column('rows_out', sa.BIGINT(), autoincrement=False, nullable=True, comment='Total rows output to Postgres'),
    sa.Column('bytes_in', sa.BIGINT(), autoincrement=False, nullable=True, comment='Total bytes input from origin'),
    sa.Column('bytes_out', sa.BIGINT(), autoincrement=False, nullable=True, comment='Total bytes output to Postgres'),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True, comment='Metadata specific for the FDW'),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('fdw_name', name='wrappers_fdw_stats_pkey'),
    comment='Wrappers Foreign Data Wrapper statistics'
    )
    op.drop_table('Recipe_type')
    op.drop_table('Recipe_tag')
    op.drop_table('Recipe_origin')
    op.drop_table('Recipe_ingredient')
    op.drop_table('Recipe_category')
    op.drop_table('Rate')
    op.drop_table('Nutrition')
    op.drop_table('Like')
    op.drop_table('Comment')
    op.drop_table('Attachment')
    op.drop_table('Socials')
    op.drop_table('Recipe')
    op.drop_table('Following')
    op.drop_table('User')
    op.drop_table('Type')
    op.drop_table('Tag')
    op.drop_table('Origin')
    op.drop_table('Ingredient')
    op.drop_table('Category')
    # ### end Alembic commands ###

"""add foreign key to posts table

Revision ID: 7eeeac51bd67
Revises: 391dbb5a33c1
Create Date: 2022-04-06 16:48:28.021430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eeeac51bd67'
down_revision = '391dbb5a33c1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table="users", local_cols = ['owner_id'], remote_cols = ['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

"""add information to post

Revision ID: 8b72afc19e51
Revises: 32c5078eb691
Create Date: 2022-04-06 16:32:58.710980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b72afc19e51'
down_revision = '32c5078eb691'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

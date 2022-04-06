"""add users table

Revision ID: 391dbb5a33c1
Revises: 8b72afc19e51
Create Date: 2022-04-06 16:42:04.543005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '391dbb5a33c1'
down_revision = '8b72afc19e51'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass

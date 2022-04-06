"""autovote

Revision ID: 35654170b0e3
Revises: 6a54a0be43a8
Create Date: 2022-04-06 17:13:06.755535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35654170b0e3'
down_revision = '6a54a0be43a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('posts', sa.Column('information', sa.String(), nullable=False))
    op.drop_column('posts', 'content')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('posts', 'information')
    op.drop_table('votes')
    # ### end Alembic commands ###

"""add like table

Revision ID: 689e53944df9
Revises: 366ac369794a
Create Date: 2026-07-23 13:08:15.060587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689e53944df9'
down_revision = '366ac369794a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('like',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['post.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like')
    )


def downgrade():
    op.drop_table('like')

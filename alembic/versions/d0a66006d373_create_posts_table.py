"""create posts table

Revision ID: d0a66006d373
Revises: 
Create Date: 2026-10-01 16:57:44.481013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0a66006d373'
# down_revision = None   # اولین migration است، پس قبلی ندارد

down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    # op.create_table(
    #     'users',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('email', sa.String(), nullable=True),
    #     sa.Column('password', sa.String(), nullable=False),
    #     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
    #               server_default=sa.text('now()'), nullable=True),
    #     sa.PrimaryKeyConstraint('id'),
    #     sa.UniqueConstraint('email'),
    # )
    #
    # op.create_table(
    #     'posts',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('title', sa.String(), nullable=False),
    #     sa.Column('content', sa.String(), nullable=False),
    #     sa.Column('published', sa.Boolean(), server_default='true', nullable=True),
    #     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
    #               server_default=sa.text('now()'), nullable=True),
    #     sa.Column('owner_id', sa.Integer(), nullable=False),
    #     sa.PrimaryKeyConstraint('id'),
    #     sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    # )
    #
    # op.create_table(
    #     'votes',
    #     sa.Column('post_id', sa.Integer(), nullable=False),
    #     sa.Column('user_id', sa.Integer(), nullable=False),
    #     sa.PrimaryKeyConstraint('post_id', 'user_id'),
    #     sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    #     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    # )
    pass



def downgrade():
    """Downgrade schema."""
    # op.drop_table('votes')
    # op.drop_table('posts')
    # op.drop_table('users')
    pass
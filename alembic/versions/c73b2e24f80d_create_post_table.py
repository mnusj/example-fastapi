"""create post table

Revision ID: c73b2e24f80d
Revises: 
Create Date: 2026-10-14 11:47:39.280820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c73b2e24f80d'  # revision ID for this migration
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass

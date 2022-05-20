"""add fkey to posts table

Revision ID: ce6821ec90fa
Revises: c8a8c1128b6a
Create Date: 2022-05-17 12:30:32.680153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce6821ec90fa'
down_revision = 'c8a8c1128b6a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts", referent_table="users",
     local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id') 
    pass

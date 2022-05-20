"""add content column to post table

Revision ID: 7f29384ca215
Revises: c3e5809795ef
Create Date: 2022-05-17 12:10:10.470459

"""
from logging import NullHandler
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f29384ca215'
down_revision = 'c3e5809795ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass

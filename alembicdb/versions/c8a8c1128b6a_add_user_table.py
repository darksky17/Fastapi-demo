"""add user table

Revision ID: c8a8c1128b6a
Revises: 7f29384ca215
Create Date: 2022-05-17 12:19:04.378267

"""
from operator import truediv
from time import time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a8c1128b6a'
down_revision = '7f29384ca215'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String(),nullable=False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )
    pass


def downgrade():
    op.drop_table('users')
    pass

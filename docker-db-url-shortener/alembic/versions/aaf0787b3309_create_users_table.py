"""create users table

Revision ID: aaf0787b3309
Revises: 
Create Date: 2022-10-01 10:49:38.050823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaf0787b3309'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('user_id', sa.BigInteger, primary_key=True),
        sa.Column('email', sa.String(64), nullable=False),
        sa.Column('created_timestamp', sa.DateTime),
        sa.Column('updated_timestamp', sa.DateTime)
    )


def downgrade():
    op.drop_table('users')

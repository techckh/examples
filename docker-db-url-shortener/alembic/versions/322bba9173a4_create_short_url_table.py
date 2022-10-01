"""create short url table

Revision ID: 322bba9173a4
Revises: aaf0787b3309
Create Date: 2022-10-01 11:35:47.553747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '322bba9173a4'
down_revision = 'aaf0787b3309'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'short_urls',
        sa.Column('url_id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.user_id')),
        sa.Column('original_url', sa.String(512)),
        sa.Column('created_timestamp', sa.DateTime),
        sa.Column('expire_timestamp', sa.DateTime)
    )


def downgrade():
    op.drop_table('short_urls')

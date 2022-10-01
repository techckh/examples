"""create click metrics table

Revision ID: 28f4164627ee
Revises: 322bba9173a4
Create Date: 2022-10-01 11:48:53.505693

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '28f4164627ee'
down_revision = '322bba9173a4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'click_metrics',
        sa.Column('metric_id', sa.BigInteger, primary_key=True),
        sa.Column('url_id', sa.BigInteger, sa.ForeignKey('short_urls.url_id')),
        sa.Column('user_ip', postgresql.CIDR),
        sa.Column('metric_type', sa.String(64)),
        sa.Column('timestamp', sa.DateTime),
    )


def downgrade():
    op.drop_table('click_metrics')

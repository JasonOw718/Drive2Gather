"""Add verification_status to driver table

Revision ID: add_verification_status_to_driver
Revises: add_payment_method_to_donation
Create Date: 2023-07-29 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_verification_status_to_driver'
down_revision = 'add_payment_method_to_donation'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('driver', sa.Column('verification_status', sa.String(length=20), nullable=False, server_default='pending'))


def downgrade():
    op.drop_column('driver', 'verification_status') 
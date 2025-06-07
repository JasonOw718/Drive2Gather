"""Add payment_method to donation table

Revision ID: add_payment_method_to_donation
Revises: 
Create Date: 2023-07-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_payment_method_to_donation'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('donation', sa.Column('payment_method', sa.String(length=50), nullable=True, server_default='stripe'))


def downgrade():
    op.drop_column('donation', 'payment_method') 
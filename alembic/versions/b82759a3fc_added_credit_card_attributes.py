"""Added credit card attributes

Revision ID: b82759a3fc
Revises: 71ccc30a60
Create Date: 2015-07-18 14:23:05.365219

"""

# revision identifiers, used by Alembic.
revision = 'b82759a3fc'
down_revision = '71ccc30a60'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


# noinspection PyUnresolvedReferences
def upgrade():
    op.add_column('credit_accounts', sa.Column('apr_pct', sa.Integer(), nullable=True))
    op.add_column('credit_accounts', sa.Column('balance', sa.Integer(), nullable=True))
    op.add_column('credit_accounts', sa.Column('credit_limit', sa.Integer(), nullable=True))
    op.add_column('credit_accounts', sa.Column('minimum_payment', sa.Integer(), nullable=True))


# noinspection PyUnresolvedReferences
def downgrade():
    op.drop_column('credit_accounts', 'minimum_payment')
    op.drop_column('credit_accounts', 'credit_limit')
    op.drop_column('credit_accounts', 'balance')
    op.drop_column('credit_accounts', 'apr_pct')

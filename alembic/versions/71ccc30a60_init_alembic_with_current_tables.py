"""Init alembic with current tables.

Revision ID: 71ccc30a60
Revises: 
Create Date: 2015-07-18 12:00:04.658771

"""

# revision identifiers, used by Alembic.
revision = '71ccc30a60'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


# noinspection PyUnresolvedReferences
def upgrade():
    # op.create_table(
    #     'pay_periods',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('name', sa.String(), nullable=False),
    #     sa.Column('checks_year', sa.Integer(), nullable=True),
    #     sa.PrimaryKeyConstraint('id'),
    #     sa.UniqueConstraint('name')
    # )
    #
    # op.create_table(
    #     'time_periods',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('name', sa.String(), nullable=False),
    #     sa.Column('occurrence_year', sa.Integer(), nullable=True),
    #     sa.PrimaryKeyConstraint('id'),
    #     sa.UniqueConstraint('name')
    # )
    #
    op.create_table(
        'time_periods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('occurrence_per_year', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'credit_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('time_period_id', sa.Integer(), nullable=True),
        sa.Column('has_auto_pay', sa.Boolean(), nullable=True),
        sa.Column('auto_pay_enabled', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['time_period_id'], ['time_periods.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'earners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('gross_annual', sa.Integer(), nullable=True),
        sa.Column('time_period_id', sa.Integer(), nullable=True),
        sa.Column('net_paycheck', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['time_period_id'], ['time_periods.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('time_period_id', sa.Integer(), nullable=True),
        sa.Column('has_auto_pay', sa.Boolean(), nullable=True),
        sa.Column('auto_pay_enabled', sa.Boolean(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['time_period_id'], ['time_periods.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'ministries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('time_period_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['time_period_id'], ['time_periods.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )


# noinspection PyUnresolvedReferences
def downgrade():
    op.drop_table('ministries')
    op.drop_table('expenses')
    op.drop_table('earners')
    op.drop_table('credit_accounts')
    op.drop_table('time_periods')

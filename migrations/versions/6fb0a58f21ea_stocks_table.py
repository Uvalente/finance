"""Stocks table

Revision ID: 6fb0a58f21ea
Revises: 67900a207d0d
Create Date: 2020-07-12 12:24:10.099378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fb0a58f21ea'
down_revision = '67900a207d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=20), nullable=False),
    sa.Column('shares', sa.Integer(), nullable=True),
    sa.Column('buy_price', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_symbol'), 'stocks', ['symbol'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stocks_symbol'), table_name='stocks')
    op.drop_table('stocks')
    # ### end Alembic commands ###
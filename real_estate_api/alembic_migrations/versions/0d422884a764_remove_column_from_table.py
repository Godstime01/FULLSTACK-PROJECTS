"""Remove column from table

Revision ID: 0d422884a764
Revises: 1526bdf6e778
Create Date: 2024-04-29 07:50:11.594143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d422884a764'
down_revision: Union[str, None] = '1526bdf6e778'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_otp',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=6), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_user_otp_id'), 'user_otp', ['id'], unique=False)
    op.drop_column('users', 'date_joined')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date_joined', sa.TIMESTAMP(), server_default=sa.text('(now())'), nullable=True))
    op.drop_index(op.f('ix_user_otp_id'), table_name='user_otp')
    op.drop_table('user_otp')
    # ### end Alembic commands ###
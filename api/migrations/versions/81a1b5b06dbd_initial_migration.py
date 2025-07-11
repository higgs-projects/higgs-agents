"""Initial migration

Revision ID: 81a1b5b06dbd
Revises: 
Create Date: 2025-07-12 19:24:39.215233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# 就是加了这一行
import sqlmodel.sql.sqltypes



# revision identifiers, used by Alembic.
revision: str = '81a1b5b06dbd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hero',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('secret_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('hero_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hero')
    # ### end Alembic commands ###

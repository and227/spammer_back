"""empty message

Revision ID: 6bd449e01e71
Revises: 
Create Date: 2021-07-06 20:11:05.580434

"""
from alembic import op
import sqlalchemy as sa

from schemas.spammer import SpammerStateEnum

# revision identifiers, used by Alembic.
revision = '6bd449e01e71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    spammer_type_enum = sa.Enum(
        SpammerStateEnum,
        name='spammer_type_enum'
    )
    op.create_table('spammer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('spammer_type', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('target', sa.String(), nullable=True),
    sa.Column('target_type', sa.String(), nullable=True),
    sa.Column('current', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    # sa.Column('state', sa.Enum('working', 'stopped', name='spammerstateenum'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usertable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('hashed_password')
    )
    # ### end Alembic commands ###

    op.add_column(
        'spammer', 
        sa.Column("state", spammer_type_enum,
        default=SpammerStateEnum.stopped
    ))

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usertable')
    op.drop_table('spammer')
    # ### end Alembic commands ###

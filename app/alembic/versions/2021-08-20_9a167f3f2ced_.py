"""empty message

Revision ID: 9a167f3f2ced
Revises: f0d5915490c7
Create Date: 2021-08-20 07:25:08.379403

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9a167f3f2ced'
down_revision = 'f0d5915490c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spammer', sa.Column('options', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('spammer', sa.Column('password', sa.String(), nullable=True))
    op.add_column('spammer', sa.Column('script_template', sa.String(), nullable=True))
    op.add_column('spammer', sa.Column('statistics', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.drop_column('spammer', 'total')
    op.drop_column('spammer', 'spammer_type')
    op.drop_column('spammer', 'current')
    op.drop_column('spammer', 'target_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spammer', sa.Column('target_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('spammer', sa.Column('current', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('spammer', sa.Column('spammer_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('spammer', sa.Column('total', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('spammer', 'statistics')
    op.drop_column('spammer', 'script_template')
    op.drop_column('spammer', 'password')
    op.drop_column('spammer', 'options')
    # ### end Alembic commands ###

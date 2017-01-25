"""User account roles

Revision ID: 2d9bf123d5b7
Revises: 5bf4f9988d35
Create Date: 2017-01-25 16:33:24.587672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d9bf123d5b7'
down_revision = '5bf4f9988d35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('RolesAccounts',
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['UserAccount.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], )
    )
    op.add_column('UserAccount', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserAccount', 'active')
    op.drop_table('RolesAccounts')
    op.drop_table('Role')
    # ### end Alembic commands ###
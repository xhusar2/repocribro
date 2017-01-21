"""User and UserAccount init

Revision ID: b54933ca6e01
Revises: 
Create Date: 2017-01-20 19:55:12.581730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b54933ca6e01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UserAccount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('GH_User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('login', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('company', sa.UnicodeText(), nullable=True),
    sa.Column('location', sa.UnicodeText(), nullable=True),
    sa.Column('bio', sa.UnicodeText(), nullable=True),
    sa.Column('blog_url', sa.UnicodeText(), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.Column('hireable', sa.Boolean(), nullable=True),
    sa.Column('user_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_account_id'], ['UserAccount.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('github_id'),
    sa.UniqueConstraint('login')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('GH_User')
    op.drop_table('UserAccount')
    # ### end Alembic commands ###
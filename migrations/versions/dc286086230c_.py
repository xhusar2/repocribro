"""Initial DB

Revision ID: dc286086230c
Revises: 
Create Date: 2018-07-06 09:34:52.932029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc286086230c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('UserAccount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('RepositoryOwner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('login', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('company', sa.UnicodeText(), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('location', sa.UnicodeText(), nullable=True),
    sa.Column('blog_url', sa.UnicodeText(), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.Column('hireable', sa.Boolean(), nullable=True),
    sa.Column('user_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_account_id'], ['UserAccount.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('github_id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('RolesAccounts',
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['UserAccount.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['Role.id'], )
    )
    op.create_table('Repository',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('fork_of', sa.Integer(), nullable=True),
    sa.Column('full_name', sa.String(length=150), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('languages', sa.UnicodeText(), nullable=True),
    sa.Column('url', sa.UnicodeText(), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('private', sa.Boolean(), nullable=True),
    sa.Column('visibility_type', sa.Integer(), nullable=True),
    sa.Column('secret', sa.String(length=255), nullable=True),
    sa.Column('webhook_id', sa.Integer(), nullable=True),
    sa.Column('last_event', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['RepositoryOwner.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name'),
    sa.UniqueConstraint('github_id'),
    sa.UniqueConstraint('secret')
    )
    op.create_table('Push',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('ref', sa.String(length=255), nullable=True),
    sa.Column('after', sa.String(length=255), nullable=True),
    sa.Column('before', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('distinct_size', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sender_login', sa.String(length=40), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repository_id'], ['Repository.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('github_id', sa.Integer(), nullable=True),
    sa.Column('tag_name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.String(length=60), nullable=True),
    sa.Column('published_at', sa.String(length=60), nullable=True),
    sa.Column('url', sa.UnicodeText(), nullable=True),
    sa.Column('prerelease', sa.Boolean(), nullable=True),
    sa.Column('draft', sa.Boolean(), nullable=True),
    sa.Column('name', sa.UnicodeText(), nullable=True),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.Column('author_login', sa.String(length=40), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('sender_login', sa.String(length=40), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repository_id'], ['Repository.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ReposMembers',
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['repository_id'], ['Repository.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['RepositoryOwner.id'], )
    )
    op.create_table('Commit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sha', sa.String(length=40), nullable=True),
    sa.Column('message', sa.UnicodeText(), nullable=True),
    sa.Column('author_name', sa.UnicodeText(), nullable=True),
    sa.Column('author_email', sa.String(length=255), nullable=True),
    sa.Column('distinct', sa.Boolean(), nullable=True),
    sa.Column('push_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['push_id'], ['Push.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Commit')
    op.drop_table('ReposMembers')
    op.drop_table('Release')
    op.drop_table('Push')
    op.drop_table('Repository')
    op.drop_table('RolesAccounts')
    op.drop_table('RepositoryOwner')
    op.drop_table('UserAccount')
    op.drop_table('Role')
    # ### end Alembic commands ###
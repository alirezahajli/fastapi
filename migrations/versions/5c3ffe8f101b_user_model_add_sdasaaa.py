"""user model add sdasaaa

Revision ID: 5c3ffe8f101b
Revises: d7c34b9f238b
Create Date: 2021-12-13 14:44:37.484624

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             


# revision identifiers, used by Alembic.
revision = '5c3ffe8f101b'
down_revision = 'd7c34b9f238b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_url_test', table_name='url')
    op.drop_column('url', 'test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('test', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_index('ix_url_test', 'url', ['test'], unique=False)
    # ### end Alembic commands ###

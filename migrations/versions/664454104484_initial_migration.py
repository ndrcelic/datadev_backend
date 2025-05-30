"""Initial migration

Revision ID: 664454104484
Revises: 
Create Date: 2025-05-09 22:31:34.488070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '664454104484'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('annotation', sa.String(length=255), nullable=True),
    sa.Column('extension', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###

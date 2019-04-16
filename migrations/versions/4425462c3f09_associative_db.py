"""associative DB

Revision ID: 4425462c3f09
Revises: f497469e48e8
Create Date: 2018-12-24 10:26:32.965769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4425462c3f09'
down_revision = 'f497469e48e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.create_table('profiles',
    sa.Column('profile_id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=255), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('profile_id')
    )
    # ### end Alembic commands ###

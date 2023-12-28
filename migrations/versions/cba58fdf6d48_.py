"""empty message

Revision ID: cba58fdf6d48
Revises: d0bbda3ba2bc
Create Date: 2023-12-28 20:15:27.477414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba58fdf6d48'
down_revision = 'd0bbda3ba2bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pro_bono', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=3000),
               type_=sa.String(length=650),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pro_bono', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=650),
               type_=sa.VARCHAR(length=3000),
               existing_nullable=False)

    # ### end Alembic commands ###

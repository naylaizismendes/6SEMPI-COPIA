"""empty message

Revision ID: d20c6fa17ea2
Revises: 65c1b732abb7
Create Date: 2024-11-28 12:59:57.771990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd20c6fa17ea2'
down_revision = '65c1b732abb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fornecedora', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.alter_column('cnpj',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fornecedora', schema=None) as batch_op:
        batch_op.alter_column('cnpj',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('telefone',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
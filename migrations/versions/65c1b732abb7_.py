"""empty message

Revision ID: 65c1b732abb7
Revises: 2535c8a0345a
Create Date: 2024-11-28 11:18:00.189185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65c1b732abb7'
down_revision = '2535c8a0345a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto_fornecedor',
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('fornecedora_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fornecedora_id'], ['fornecedora.id'], ),
    sa.ForeignKeyConstraint(['produto_id'], ['produto.id'], ),
    sa.PrimaryKeyConstraint('produto_id', 'fornecedora_id')
    )
    with op.batch_alter_table('fornecedora', schema=None) as batch_op:
        batch_op.alter_column('endereco',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('cidade',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fornecedora', schema=None) as batch_op:
        batch_op.alter_column('cidade',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('endereco',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    op.drop_table('produto_fornecedor')
    # ### end Alembic commands ###

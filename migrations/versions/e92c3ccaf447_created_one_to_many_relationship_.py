"""Created one to many relationship between Cat and Caretaker

Revision ID: e92c3ccaf447
Revises: 7b406d48aa56
Create Date: 2022-05-10 10:12:41.365236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e92c3ccaf447'
down_revision = '7b406d48aa56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cat', sa.Column('caretaker_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cat', 'caretaker', ['caretaker_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cat', type_='foreignkey')
    op.drop_column('cat', 'caretaker_id')
    # ### end Alembic commands ###
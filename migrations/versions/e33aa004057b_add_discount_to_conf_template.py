"""add discount to conf_template

Revision ID: e33aa004057b
Revises: 2a3369d396fe
Create Date: 2025-05-10 20:10:58.210011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e33aa004057b'
down_revision = '2a3369d396fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_has_conf_template',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('conf_template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['conf_template_id'], ['conf_template.id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.PrimaryKeyConstraint('service_id', 'conf_template_id')
    )
    op.create_table('vm_service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vm_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['service.id'], ),
    sa.ForeignKeyConstraint(['vm_id'], ['vm.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('conf_template', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discount', sa.Integer(), nullable=True))

    with op.batch_alter_table('vm', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discount', sa.String(length=45), nullable=True))
        batch_op.add_column(sa.Column('id_conf_templates', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'conf_template', ['id_conf_templates'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vm', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('id_conf_templates')
        batch_op.drop_column('discount')

    with op.batch_alter_table('conf_template', schema=None) as batch_op:
        batch_op.drop_column('discount')

    op.drop_table('vm_service')
    op.drop_table('service_has_conf_template')
    op.drop_table('service')
    # ### end Alembic commands ###

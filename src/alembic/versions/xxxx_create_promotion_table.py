from alembic import op
import sqlalchemy as sa

revision = '0001_create_promotions'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'promotions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.String(255)),
        sa.Column('discount_type', sa.String(20), nullable=False),  # e.g., 'percentage', 'fixed'
        sa.Column('discount_value', sa.Float, nullable=False),
        sa.Column('valid_from', sa.DateTime, nullable=False),
        sa.Column('valid_to', sa.DateTime, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('promotions')

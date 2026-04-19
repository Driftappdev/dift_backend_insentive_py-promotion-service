from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models.promotion import Base  # เปลี่ยนจาก coupon เป็น promotion
from app.config import settings

# Alembic Config object
config = context.config

# Setup logging
fileConfig(config.config_file_name)

# Metadata ของ ORM models สำหรับ autogenerate migrations
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    Generates SQL script without connecting to the database.
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    Connects to database and executes migration.
    """
    connectable = create_async_engine(settings.DATABASE_URL, future=True)

    # Use synchronous connection for Alembic
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

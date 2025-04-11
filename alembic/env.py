import os
from dotenv import load_dotenv
load_dotenv()

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.database import SQLALCHEMY_DATABASE_URL, Base

# Cargar config desde el archivo .ini
config = context.config
fileConfig(config.config_file_name)

# 🔁 IMPORTANTE: importar tu Base de modelos y el engine
from app.models.models import Base  # contiene tus modelos y declarative_base
from app.database import SQLALCHEMY_DATABASE_URL

# Establecer la metadata de los modelos como objetivo
target_metadata = Base.metadata

# Inyectar URL desde tu db.py (en lugar de hardcodearla en alembic.ini)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.base import Base          
from app.models import user, role, product, order, payment  
from app.core.config import Settings  

# Carrega configurações do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Carrega variáveis do .env via Settings()
settings = Settings()

# Define a URL de conexão do banco vinda do .env
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Define metadados para autogenerate
target_metadata = Base.metadata

# Funções de migração padrão
def run_migrations_offline() -> None:
    """Executa migrações no modo offline (gera SQL sem conectar ao banco)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações conectando ao banco (modo padrão)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Carrega as variáveis do arquivo .env (se existir)
load_dotenv()

# Postgres Connection String (lida do ambiente)
_PG_HOST = os.getenv("PG_HOST", "localhost")
_PG_PORT = os.getenv("PG_PORT", "5432")
_PG_DB = os.getenv("PG_DB", "sales_db")
_PG_USER = os.getenv("PG_USER", "postgres")
_PG_PASSWORD = os.getenv("PG_PASSWORD", "")

PG_DB_URL = f"postgresql://{_PG_USER}:{_PG_PASSWORD}@{_PG_HOST}:{_PG_PORT}/{_PG_DB}"

# SQLite Fallback Connection String
SQLITE_DB_URL = "sqlite:///sales.db"


def seed_sqlite_db(engine):
    """Popula o banco SQLite local com os dados de teste do arquivo SQL."""
    init_sql_path = os.path.join("data", "init.sql")
    if not os.path.exists(init_sql_path):
        return

    # Verifica se a tabela já possui dados
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM sales"))
            count = result.scalar()
            if count and count > 0:
                return  # Já possui dados
    except Exception:
        pass  # A tabela pode não existir, prossegue para criar

    # Lê e executa o arquivo SQL
    with open(init_sql_path, encoding="utf-8") as f:
        # Divide os comandos por ponto e vírgula
        sql_commands = f.read().split(";")

    with engine.begin() as conn:
        for command in sql_commands:
            command = command.strip()
            if command:
                conn.execute(text(command))


def get_db_engine():
    """Tenta conectar ao PostgreSQL no Docker.

    Caso falhe, utiliza o SQLite como fallback local automaticamente.
    """
    try:
        # Tenta conectar ao PostgreSQL
        engine = create_engine(PG_DB_URL)
        # Teste de conexão rápido
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conectado ao banco de dados PostgreSQL!")
        return engine
    except OperationalError:
        print(
            "Aviso: PostgreSQL indisponível. Usando banco SQLite local como fallback..."
        )
        # Cria banco SQLite local
        engine = create_engine(SQLITE_DB_URL)
        seed_sqlite_db(engine)
        return engine

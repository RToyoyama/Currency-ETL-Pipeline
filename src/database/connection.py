import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


def get_connection_string() -> str:
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'currency_db')
    user = os.getenv('POSTGRES_USER', 'airflow')
    password = os.getenv('POSTGRES_PASSWORD', 'airflow')

    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'


def get_engine() -> Engine:
    connection_string = get_connection_string()
    logger.info('Criando engine de conexão com PostgreSQL...')

    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    return engine


def test_connection() -> bool:
    try:
        engine = get_engine()

        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            logger.info(f'Conexão OK — resultado: {result.scalar()}')
            return True

    except Exception:
        logger.error('Falha na conexão: {e}')
        return False

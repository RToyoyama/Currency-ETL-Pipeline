
import pandas as pd
from sqlalchemy.engine import Engine

from src.database.connection import get_engine
from src.utils.logger import get_logger

logger = get_logger(__name__)

TABLE_NAME = "currency_rates"


def load_currency_data(df: pd.DataFrame, engine: Engine | None = None) -> int:
    if df.empty:
        logger.warning("DataFrame vazio - nada pra carregar")
        return 0

    if engine is None:
        engine = get_engine()

    logger.info(f'Carregando {len(df)} registros na tabela "{TABLE_NAME}"...')

    try:
        with engine.begin() as conn:
            rows_inserted = df.to_sql(
                name=TABLE_NAME,
                con=conn,
                if_exists="append",
                index=False,
                method="multi",
            )

        count = rows_inserted if rows_inserted is not None else len(df)
        logger.info(f"Carga concluída — {count} registros inseridos")
        return count

    except Exception as e:
        logger.error(f"Erro na carga — rollback executado: {e}")
        raise


def table_exists(engine=None) -> bool:
    from sqlalchemy import inspect

    if engine is None:
        engine = get_engine()

    inspector = inspect(engine)
    exists = TABLE_NAME in inspector.get_table_names()
    logger.info(f'Tabela "{TABLE_NAME}" existe: {exists}')
    return exists

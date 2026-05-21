from datetime import datetime

import pandas as pd
import pytest
from sqlalchemy import create_engine, engine, text

from src.load.postgres_loader import load_currency_data


@pytest.fixture
def sqlite_engine():
    engine = create_engine("sqlite:///:memory:")

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE currency_rates (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                currency     TEXT NOT NULL,
                value        REAL NOT NULL,
                collected_at TEXT NOT NULL
            )
        """))

    return engine


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "currency": ["USD-BRL", "EUR-BRL", "BTC-BRL"],
            "value": [5.09, 5.58, 217500.0],
            "collected_at": [
                datetime(2024, 1, 1, 9, 0, 0),
                datetime(2024, 1, 1, 9, 0, 0),
                datetime(2024, 1, 1, 9, 0, 0),
            ],
        }
    )


def test_load_dataframe_vazio_retorna_zero(sqlite_engine) -> None:
    df_vazio = pd.DataFrame(columns=["currency", "value", "collected_at"])
    result = load_currency_data(df_vazio, engine=sqlite_engine)
    assert result == 0


def test_load_acumulativo(sqlite_engine, sample_dataframe) -> None:
    load_currency_data(sample_dataframe, engine=sqlite_engine)
    load_currency_data(sample_dataframe, engine=sqlite_engine)

    with sqlite_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM currency_rates"))
        count = result.scalar()

    assert count == 6


def test_load_retorna_numero_de_registros(sqlite_engine, sample_dataframe) -> None:
    result = load_currency_data(sample_dataframe, engine=sqlite_engine)
    assert result == 3


def test_load_insere_dados_no_banco(sqlite_engine, sample_dataframe) -> None:
    load_currency_data(sample_dataframe, engine=sqlite_engine)

    with sqlite_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM currency_rates"))
        count = result.scalar()

    assert count == 3

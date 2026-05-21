from unittest import result

import pandas as pd
import pytest

from src import transform
from src.transform.currency_transform import transform_currency_data


def test_transform_retorna_dataframe(valid_raw_data: dict) -> None:
    result = transform_currency_data(valid_raw_data)
    assert isinstance(result, pd.DataFrame)


def test_transform_colunas_corretas(valid_raw_data: dict) -> None:
    result = transform_currency_data(valid_raw_data)
    assert set(result.columns) == {"currency", "value", "collected_at"}


def test_transform_numero_de_registros(valid_raw_data: dict) -> None:
    result = transform_currency_data(valid_raw_data)
    assert len(result) == 3


def test_transform_tipos_corretos(valid_raw_data: dict) -> None:
    result = transform_currency_data(valid_raw_data)
    assert pd.api.types.is_string_dtype(result["currency"])
    assert pd.api.types.is_float_dtype(result["value"])
    assert pd.api.types.is_datetime64_any_dtype(result["collected_at"])


def test_transform_valores_currency(valid_raw_data: dict) -> None:
    result = transform_currency_data(valid_raw_data)
    currencies = set(result["currency"].tolist())
    assert "USD-BRL" in currencies
    assert "EUR-BRL" in currencies
    assert "BTC-BRL" in currencies


def test_transform_dados_vazios_lanca_excecao() -> None:
    with pytest.raises(ValueError):
        transform_currency_data({})


def test_transform_data_inavalida_usa_fallback() -> None:
    data = {
        "USDBRL": {
            "code": "USD",
            "codein": "BRL",
            "bid": "5.09",
            "ask": "5.10",
            "timestamp": "1704067200",
            "create_date": "data-invalida",
        }
    }
    result = transform_currency_data(data)
    assert len(result) == 1
    assert pd.api.types.is_datetime64_any_dtype(result["collected_at"])

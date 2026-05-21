from datetime import datetime
from typing import Any

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def transform_currency_data(raw_data: dict[str, Any]) -> pd.DataFrame:
    if not raw_data:
        raise ValueError("Dados brutos estão vazios")

    records = []

    for pair_key, pair_data in raw_data.items():
        try:
            record = _extract_record(pair_data)
            records.append(record)
        except (KeyError, ValueError) as e:
            logger.warning(f"Par {pair_key} ignorado: {e}")
            continue

    if not records:
        raise ValueError("Nenhum registro transformado com sucesso")

    df = pd.DataFrame(records)
    df = _enforce_types(df)

    logger.info(f"Transformação concluída — {len(df)} registros")

    return df


def _extract_record(pair_data: dict[str, Any]) -> dict[str, Any]:
    currency = f'{pair_data["code"]}-{pair_data["codein"]}'
    value = float(pair_data["bid"])
    collected_at = _parse_date(pair_data.get("create_date", ""))

    return {
        "currency": currency,
        "value": value,
        "collected_at": collected_at,
    }


def _parse_date(date_str: str) -> datetime:
    if not date_str:
        logger.warning("Data ausente — usando datetime.now()")
        return datetime.now()

    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.warning(f'Data inválida: "{date_str}" — usando datetime.now()')
        return datetime.now()


def _enforce_types(df: pd.DataFrame) -> pd.DataFrame:
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["collected_at"] = pd.to_datetime(df["collected_at"])

    df_clean = df.dropna(subset=["value"])

    if len(df_clean) < len(df):
        logger.warning(
            f"{len(df) - len(df_clean)} registros removidos por valor inválido"
        )

    return df_clean.reset_index(drop=True)

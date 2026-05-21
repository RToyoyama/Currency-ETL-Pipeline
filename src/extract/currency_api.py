from http.client import REQUEST_TIMEOUT
from typing import Required
from unittest.mock import DEFAULT
from typing import Final

import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://economia.awesomeapi.com.br"
DEFAULT_PAIRS = "USD-BRL,EUR-BRL,BTC-BRL"
REQUEST_TIMEOUT: Final[int] = 10


def fetch_currency_data(pairs: str = DEFAULT_PAIRS) -> dict:
    url = f"{BASE_URL}/last/{pairs}"

    logger.info(f"Buscando cotações — URL: {url}")

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Dados recebidos — pares: {list(data.keys())}")
        return data

    except requests.Timeout:
        logger.error(f"Timeout após {REQUEST_TIMEOUT}s")
        raise

    except requests.HTTPError as e:
        logger.error(f"Erro HTTP: {e}")
        raise

    except requests.ConnectionError as e:
        logger.error(f"Erro de conexão: {e}")
        raise


def validate_raw_data(data: dict) -> bool:
    if not data:
        logger.warning(f"Dados Vazioa")
        return False

    required_fields = {"bid", "ask", "timestamp", "create_date", "code", "codein"}

    for pair_key, pair_data in data.items():
        missing = required_fields - set(pair_data.keys())
        if missing:
            logger.warning(f"{pair_key} faltando campos: {missing}")
            return False

    logger.info("Validação dos dados OK")
    return True

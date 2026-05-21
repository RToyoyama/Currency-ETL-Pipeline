import pytest


@pytest.fixture
def valid_raw_data() -> dict:
    return {
        'USDBRL': {
            'code': 'USD',
            'codein': 'BRL',
            'bid': '5.09',
            'ask': '5.10',
            'timestamp': '1704067200',
            'create_date': '2024-01-01 09:00:00',
        },
        'EURBRL': {
            'code': 'EUR',
            'codein': 'BRL',
            'bid': '5.58',
            'ask': '5.60',
            'timestamp': '1704067200',
            'create_date': '2024-01-01 09:00:00',
        },
        'BTCBRL': {
            'code': 'BTC',
            'codein': 'BRL',
            'bid': '217500',
            'ask': '217600',
            'timestamp': '1704067200',
            'create_date': '2024-01-01 09:00:00',
        },
    }

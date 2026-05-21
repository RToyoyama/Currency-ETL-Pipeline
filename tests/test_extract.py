import pytest
import requests

from src.extract.currency_api import fetch_currency_data, validate_raw_data


def test_validate_dados_validos(valid_raw_data: dict) -> None:
    result = validate_raw_data(valid_raw_data)
    assert result is True


def test_validate_dados_invalidos() -> None:
    data_incompleta = {"USDBRL": {"code": "USD"}}
    result = validate_raw_data(data_incompleta)
    assert result is False


def test_validate_dados_vazios() -> None:
    result = validate_raw_data({})
    assert result is False


def test_fetch_sucesso(mocker, valid_raw_data: dict) -> None:
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = valid_raw_data
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "src.extract.currency_api.requests.get",
        return_value=mock_response,
    )

    result = fetch_currency_data()
    assert result == valid_raw_data


def test_fetch_timeout(mocker) -> None:
    mocker.patch(
        "src.extract.currency_api.requests.get",
        side_effect=requests.Timeout(),
    )

    with pytest.raises(requests.Timeout):
        fetch_currency_data()

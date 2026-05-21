import logging
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract.currency_api import fetch_currency_data, validate_raw_data
from src.load.postgres_loader import load_currency_data, table_exists
from src.transform.currency_transform import transform_currency_data

logger = logging.getLogger(__name__)

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}


def extract(**kwargs) -> None:
    raw_data = fetch_currency_data()

    if not validate_raw_data(raw_data):
        raise ValueError("Dados da API falharam na validação")

    ti = kwargs["ti"]
    ti.xcom_push(key="row_data", value=raw_data)
    logger.info(f"Extração concluída: {list(raw_data.keys())}")


def transform(**kwargs) -> None:
    ti = kwargs["ti"]
    raw_data = ti.xcom_pull(task_id="extract_task", key="raw_data")

    if not raw_data:
        raise ValueError("Nenhum dado encontrado no XCom")

    df = transform_currency_data(raw_data)

    records = df.to_dict(orient="records")
    for record in records:
        record["collected_at"] = str(record["collected_at"])

    ti.xcom_push(key="transformed_records", value=records)
    logger.info(f"Transformação concluída: {len(records)} registros")


def load(**kwargs) -> None:
    ti = kwargs["ti"]
    records = ti.xcom_pull(task_id="transform_task", key="transform_records")

    if not records:
        raise ValueError("Nenhum registro encontrado no XCom")

    df = pd.DataFrame(records)
    df["collected_at"] = pd.to_datetime(df["collected_at"])
    df["value"] = pd.to_numeric(df["value"])

    if not table_exists:
        raise RuntimeError("Tabela currency_rates não encontrada")

    inserted = load_currency_data(df)
    logger.info(f"Carga concluída: {inserted} registros inseridos")


with DAG(
    dag_id="currency_etl_pipeline",
    description="Pipeline ETL de cotações de moedas",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["etl", "currency"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task

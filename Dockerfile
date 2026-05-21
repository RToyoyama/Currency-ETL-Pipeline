FROM apache/airflow:2.9.2-python3.12

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/airflow

COPY pyproject.toml .

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    requests \
    python-dotenv

COPY src/ ./src/
COPY dags/ ./dags/
COPY sql/ ./sql/

ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
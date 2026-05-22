# Currency ETL Pipeline

[![CI](https://github.com/RToyoyama/Currency-ETL-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/RToyoyama/Currency-ETL-Pipeline/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9-017CEE?logo=apacheairflow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Ruff](https://img.shields.io/badge/Lint-Ruff-D7FF64?logo=ruff)

Pipeline ETL automatizado que coleta cotações de moedas em tempo real, transforma os dados e os persiste em PostgreSQL — tudo orquestrado pelo Apache Airflow e containerizado com Docker.

---

## Sobre o Projeto

Este projeto foi desenvolvido com foco em **Engenharia de Dados**, aplicando boas práticas de mercado em um pipeline ETL completo:

- Coleta automática de cotações de **USD, EUR e BTC** em reais
- Transformação e limpeza dos dados com **Pandas**
- Persistência em **PostgreSQL**
- Orquestração com **Apache Airflow** — execução a cada hora
- Containerização completa com **Docker Compose**
- Pipeline de **CI/CD** com **GitHub Actions**
- Testes automatizados com **Pytest**
- Qualidade de código com **Ruff**

---

## Arquitetura

```
API (AwesomeAPI)
      │
      ▼
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Extract   │────▶│    Transform    │────▶│     Load     │
│             │     │                 │     │              │
│ Requests    │     │ Pandas          │     │ SQLAlchemy   │
│ Validação   │     │ Tipagem         │     │ PostgreSQL   │
└─────────────┘     └─────────────────┘     └──────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │     Apache Airflow      │
              │  Orquestração @hourly   │
              │  Retries automáticos    │
              │  Monitoramento via UI   │
              └─────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │      Docker Compose     │
              │  postgres               │
              │  airflow-webserver      │
              │  airflow-scheduler      │
              └─────────────────────────┘
```

---

## Estrutura do Projeto

```
Currency-ETL-Pipeline/
│
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD
│
├── dags/
│   └── currency_dag.py         # DAG do Airflow
│
├── src/
│   ├── extract/
│   │   └── currency_api.py     # Consumo da API
│   ├── transform/
│   │   └── currency_transform.py  # Transformação com Pandas
│   ├── load/
│   │   └── postgres_loader.py  # Carga no PostgreSQL
│   ├── database/
│   │   └── connection.py       # Conexão via SQLAlchemy
│   └── utils/
│       └── logger.py           # Logger centralizado
│
├── tests/
│   ├── conftest.py             # Fixtures compartilhadas
│   ├── test_extract.py         # Testes de extração
│   ├── test_transform.py       # Testes de transformação
│   └── test_load.py            # Testes de carga
│
├── sql/
│   └── create_tables.sql       # DDL do banco de dados
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

---

## Tecnologias

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.13 | Linguagem principal |
| uv | latest | Gerenciamento de dependências |
| Apache Airflow | 2.9.2 | Orquestração do pipeline |
| PostgreSQL | 15 | Armazenamento dos dados |
| Pandas | 2.2+ | Transformação dos dados |
| SQLAlchemy | 2.0+ | Abstração do banco de dados |
| Docker / Compose | latest | Containerização |
| Pytest | 8.0+ | Testes automatizados |
| Ruff | 0.4+ | Lint e formatação |
| GitHub Actions | — | CI/CD |

---

## Dados Coletados

| Par | Descrição | Frequência |
|---|---|---|
| USD-BRL | Dólar Americano → Real | A cada hora |
| EUR-BRL | Euro → Real | A cada hora |
| BTC-BRL | Bitcoin → Real | A cada hora |

Fonte: [AwesomeAPI](https://economia.awesomeapi.com.br/)

---

## Como Executar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- [Git](https://git-scm.com/)

### 1. Clone o repositório

```bash
git clone https://github.com/RToyoyama/Currency-ETL-Pipeline.git
cd Currency-ETL-Pipeline
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

### 3. Suba os containers

```bash
docker compose up -d
```

A primeira execução demora alguns minutos — o Docker precisa baixar e construir as imagens.

### 4. Aguarde a inicialização

```bash
docker compose logs -f airflow-webserver
```

Aguarde até aparecer: `Listening at: http://0.0.0.0:8080`

### 5. Acesse o Airflow

- URL: [http://localhost:8080](http://localhost:8080)
- Usuário: `admin`
- Senha: `admin`

### 6. Ative o pipeline

Na interface do Airflow, ative a DAG `currency_etl_pipeline` e clique em ▶ para executar manualmente.

### 7. Consulte os dados

```bash
docker exec -it currency-postgres psql -U airflow -d airflow \
  -c "SELECT * FROM currency_rates ORDER BY collected_at DESC LIMIT 10;"
```

---

## Testes

```bash
# Instalar dependências de desenvolvimento
uv sync --dev

# Executar todos os testes
uv run pytest -v
```

Os testes rodam sem dependências externas — a API é mockada e o banco é SQLite em memória.

---

## CI/CD

O pipeline de CI executa automaticamente a cada push e pull request:

1. **Lint** — `ruff check .`
2. **Formatação** — `ruff format --check .`
3. **Testes** — `pytest -v`

---

## Schema do Banco de Dados

```sql
CREATE TABLE currency_rates (
    id           SERIAL PRIMARY KEY,
    currency     VARCHAR(20)    NOT NULL,
    value        NUMERIC(10, 2) NOT NULL,
    collected_at TIMESTAMP      NOT NULL
);
```

---

## Evoluções Futuras

- [ ] Camada raw — preservar dados brutos da API em Parquet
- [ ] Idempotência — evitar inserção de duplicatas
- [ ] Great Expectations — validação de qualidade dos dados
- [ ] MinIO — Data Lake local para arquivos intermediários
- [ ] Alertas — notificações por e-mail em caso de falha
- [ ] Dashboard — visualização das cotações históricas

---

## Autor

**Renan Toyoyama**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/renan-toyoyama-3b0165308/)
[![GitHub](https://img.shields.io/badge/GitHub-RToyoyama-181717?logo=github)](https://github.com/RToyoyama)
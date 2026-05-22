CREATE TABLE IF NOT EXISTS currency_rates (
    id              SERIAL PRIMARY KEY,
    currency        VARCHAR(20)     NOT NULL,
    value           NUMERIC(10,2)   NOT NULL,
    collected_at    TIMESTAMP       NOT NULL
);
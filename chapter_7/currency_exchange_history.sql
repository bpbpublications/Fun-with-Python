CREATE TABLE IF NOT EXISTS currency_exchange_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_code TEXT,
    last_price FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT constraint_name UNIQUE (currency_code, updated_at)
);

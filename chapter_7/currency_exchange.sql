CREATE TABLE IF NOT EXISTS currency_exchange (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_code TEXT UNIQUE,
    last_price FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

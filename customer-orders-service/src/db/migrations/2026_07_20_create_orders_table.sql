CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id);

import sqlite3
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db.models import Base, Order


def test_orders_table_is_created_with_expected_columns():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        order = Order(customer_id=1, order_date="2026-07-19", amount=42.5, status="pending")
        session.add(order)
        session.commit()
        assert order.id is not None

    migration_path = ROOT / "src" / "db" / "migrations" / "2026_07_20_create_orders_table.sql"
    db_path = ROOT / "tests" / "orders_test.db"
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        conn.executescript(migration_path.read_text())
        cursor = conn.execute("PRAGMA table_info(orders)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert set(columns) == {"id", "customer_id", "order_date", "amount", "status"}
    assert columns["id"] == "INTEGER"
    assert columns["customer_id"] == "INTEGER"
    assert columns["order_date"] == "TEXT"
    assert columns["amount"] == "REAL"
    assert columns["status"] == "TEXT"

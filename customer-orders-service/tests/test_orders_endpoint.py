import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api.orders import ENGINE
from src.db.models import Base, Order
from src.main import app


client = TestClient(app)


def test_orders_endpoint_returns_paginated_orders():
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)

    with Session(ENGINE) as session:
        session.add_all(
            [
                Order(customer_id=1, order_date="2026-07-01", amount=10.0, status="pending"),
                Order(customer_id=1, order_date="2026-07-02", amount=20.0, status="delivered"),
            ]
        )
        session.commit()

    response = client.get("/orders?customer_id=1&page=1&page_size=1")
    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 1
    assert payload["page_size"] == 1
    assert len(payload["orders"]) == 1


def test_orders_endpoint_returns_400_for_invalid_page():
    response = client.get("/orders?page=0")
    assert response.status_code == 400

import sys
from pathlib import Path

from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api.orders import ENGINE
from src.db.models import Base, Order
from src.repositories.orders_repository import OrdersRepository


def test_repository_filters_and_paginate_orders():
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)

    with Session(ENGINE) as session:
        session.add_all(
            [
                Order(customer_id=1, order_date="2026-07-01", amount=10.0, status="pending"),
                Order(customer_id=1, order_date="2026-07-02", amount=20.0, status="delivered"),
                Order(customer_id=1, order_date="2026-07-03", amount=30.0, status="pending"),
                Order(customer_id=2, order_date="2026-07-04", amount=40.0, status="pending"),
            ]
        )
        session.commit()

        repository = OrdersRepository(session)
        orders, total_count = repository.get_orders_by_customer("1", "pending", 1, 2)

        assert len(orders) == 2
        assert total_count == 2
        assert all(order["customer_id"] == 1 for order in orders)
        assert all(order["status"] == "pending" for order in orders)

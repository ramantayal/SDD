from __future__ import annotations

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.models import Order


class OrdersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_orders_by_customer(
        self,
        customer_id: str,
        status: Optional[str],
        page: int,
        page_size: int,
    ) -> tuple[list[dict], int]:
        query = select(Order).where(Order.customer_id == int(customer_id))

        if status:
            query = query.where(Order.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        total_count = int(self.session.scalar(count_query) or 0)

        filtered_query = query.order_by(Order.id.asc())
        offset = (page - 1) * page_size
        paged_query = filtered_query.offset(offset).limit(page_size)
        rows = self.session.execute(paged_query).scalars().all()

        orders = [
            {
                "id": row.id,
                "customer_id": row.customer_id,
                "order_date": row.order_date,
                "amount": float(row.amount),
                "status": row.status,
            }
            for row in rows
        ]
        return orders, total_count

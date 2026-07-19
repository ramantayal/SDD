from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.models import Base
from src.repositories.orders_repository import OrdersRepository

router = APIRouter()

DB_PATH = Path(__file__).resolve().parents[1] / "orders.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(ENGINE)


def get_db() -> Session:
    session = Session(ENGINE)
    try:
        yield session
    finally:
        session.close()


@router.get("/orders")
def list_orders(
    customer_id: str = Query(default="1"),
    status_filter: Optional[str] = None,
    page: int = Query(default=1),
    page_size: int = Query(default=10),
    db: Session = Depends(get_db),
):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page must be greater than 0")
    if page_size < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page_size must be greater than 0")

    repository = OrdersRepository(db)
    orders, total_count = repository.get_orders_by_customer(customer_id, status_filter, page, page_size)
    return {
        "orders": orders,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
    }

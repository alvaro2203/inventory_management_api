from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from inventory_management.models.product import Product
from inventory_management.models.stock_movements import StockMovement


def get_db_products(
        db: Session,
        skip: int = 0,
        limit: int = 0,
        category_id: Optional[int] = None,
        search_name: Optional[str] = None,
) -> List[Product]:
    statement = (
        select(Product)
        .options(selectinload(Product.category))
        .options(selectinload(Product.provider))
        .options(selectinload(Product.stock_movements))
    )

    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)

    if search_name:
        statement = statement.where(Product.name.ilike(f"%{search_name}"))

    statement.offset(skip).limit(limit)

    results = db.exec(statement).all()
    return results


def get_db_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    statement = select(Product).where(Product.id == product_id)

    result = db.exec(statement).first()
    return result


def get_db_product_movements(db: Session, product_id: int) -> List[StockMovement]:
    statement = select(StockMovement).where(StockMovement.product_id == product_id)

    result = db.exec(statement).all()
    return result
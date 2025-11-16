from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import field_validator

class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class StockMovement(SQLModel, table=True):
    __tablename__ = "tb_stock_movement"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(nullable=False, foreign_key="tb_product.id")
    movement_type: MovementType = Field(nullable=False)
    quantity: int = Field(nullable=False, gt=0, description="Always positive")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relationship
    product: Optional["Product"] = Relationship(back_populates="stock_movements") # type: ignore  # noqa: F821

    @field_validator("quantity")
    def validate_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be > 0")
        return quantity
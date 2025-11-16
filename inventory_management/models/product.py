from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class Product(SQLModel, table=True):
    __tablename__ = "tb_product"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    category_id: int = Field(nullable=False, foreign_key="tb_category.id")
    provider_id: Optional[int] = Field(default=None, foreign_key="tb_provider.id")

    # relationships
    category: Optional["Category"] = Relationship(back_populates="products") # type: ignore  # noqa: F821
    provider: Optional["Provider"] = Relationship(back_populates="products") # type: ignore  # noqa: F821
    stock_movements: List["StockMovement"] = Relationship(back_populates="product") # type: ignore  # noqa: F821



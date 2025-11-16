from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Category(SQLModel, table=True):
    __tablename__ = "tb_category"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    products: list["Product"] = Relationship(back_populates="category") # type: ignore  # noqa: F821

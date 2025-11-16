from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr

class Provider(SQLModel, table=True):
    __tablename__ = "tb_provider"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    contact_email: EmailStr = Field(nullable=False, unique=True, index=True)
    products: List["Product"] = Relationship(back_populates="provider") # type: ignore  # noqa: F821

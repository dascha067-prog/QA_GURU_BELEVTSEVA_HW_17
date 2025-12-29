from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str


class ProductPartial(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None

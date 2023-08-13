from typing import List
from pydantic import BaseModel

class Size(BaseModel):
    length: str
    breadth: str
    height: str

class Review(BaseModel):
    title: str
    description: str
    rating: float

class Price(BaseModel):
    mrp: float
    discounted_price: float

class Product(BaseModel):
    title: str
    brand: str
    category: str
    model: str
    size: List[Size]
    seller: str
    price: Price
    review: List[Review] | None=None
    mfg_date: str
    is_returnable: bool
    is_available: bool
    avail_quantity: int
    


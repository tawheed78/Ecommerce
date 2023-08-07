from pydantic import BaseModel
from models.user import Address

class Order(BaseModel):
    userName: str
    items: int
    address: Address
    deliveryDate: str
    price: float
    paymentMethod: str



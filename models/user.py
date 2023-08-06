from typing import List
from pydantic import BaseModel

class Name(BaseModel):
    first_name: str
    last_name: str

class Address(BaseModel):
    flat: str
    apartment: str
    road: str
    landmark: str
    city: str
    pincode: int
    state: str
    country: str


class User(BaseExceptionGroup):
    name: List[Name]
    address: List[Address]
    mobile: int
    dob: str
    gender: str
    email: str

import datetime
from pydantic import BaseModel

class Add_to_Cart(BaseModel):
    prodId : str
    userId: str
    # date: datetime

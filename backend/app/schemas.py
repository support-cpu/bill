from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    item: str
    qty: Optional[str]
    unit_price: Optional[str]
    amount: Optional[str]
    due: Optional[str]

class OrdersResponse(BaseModel):
    orders: List[OrderItem]

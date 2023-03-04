import datetime
from typing import List

from pydantic import BaseModel

from schemas.core import ListModel
from schemas.customers import CustomerBare


class OrderUpdate(BaseModel):
    identifier: int
    closed_at: datetime.datetime
    count: int


class OrderCreate(OrderUpdate):
    book_id: int
    customer_id: int


class OrderBare(OrderCreate):
    id: int
    created_at: datetime.datetime

    class Config(OrderCreate.Config):
        orm_mode = True


class OrderFull(OrderBare):
    customer: CustomerBare


class OrderList(ListModel):
    data: List[OrderBare]
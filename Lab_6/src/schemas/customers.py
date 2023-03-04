from typing import List, Optional

from pydantic import BaseModel

from schemas.core import ListModel
from schemas.users import UserBare


class CustomerUpdate(BaseModel):
    name: str
    phone: str
    address: str
    user_id: int


class CustomerCreate(CustomerUpdate):
    pass


class CustomerBare(CustomerCreate):
    id: int

    class Config(CustomerCreate.Config):
        orm_mode = True


class CustomerFull(CustomerBare):
    user: Optional[UserBare]


class CustomerList(ListModel):
    data: List[CustomerBare]

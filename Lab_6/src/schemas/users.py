from typing import List

from pydantic import BaseModel

from schemas.core import ListModel


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    middle_name: str


class UserCreate(UserUpdate):
    pass


class UserBare(UserCreate):
    id: int

    class Config(UserCreate.Config):
        orm_mode = True


class UserFull(UserBare):
    pass


class UserList(ListModel):
    data: List[UserBare]

import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.authors import AuthorBare
from schemas.core import ListModel
from schemas.orders import OrderBare


class BookUpdate(BaseModel):
    name: str
    isbn: str
    edition: int
    expenses: float
    publication_date: datetime.date
    price: float
    total_royalti: float


class BookCreate(BookUpdate):
    pass


class BookBare(BookCreate):
    id: int

    class Config(BookCreate.Config):
        orm_mode = True


class BookFull(BookBare):
    authors: List[AuthorBare] = Field(default_factory=list)
    orders: List[OrderBare] = Field(default_factory=list)


class BookList(ListModel):
    data: List[BookBare]
import datetime
from typing import List

from pydantic import BaseModel

from schemas.core import ListModel


class ContractUpdate(BaseModel):
    number: int
    signing_date: datetime.datetime
    term: int
    is_terminate: bool
    terminate_date: datetime.datetime


class ContractCreate(ContractUpdate):
    author_id: int


class ContractBare(ContractUpdate):
    id: int

    class Config(ContractUpdate.Config):
        orm_mode = True


class ContractFull(ContractBare):
    pass
    # author: AuthorBare


class ContractList(ListModel):
    data: List[ContractBare]

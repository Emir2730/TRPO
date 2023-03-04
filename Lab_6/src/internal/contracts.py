from sqlalchemy.orm import joinedload

from core.crud import CRUDPaginated
from models.publishers import Contract

contract_crud = CRUDPaginated(
    model=Contract,
    get_options=[joinedload(Contract.author)]
)
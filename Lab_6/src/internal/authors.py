from sqlalchemy.orm import joinedload, selectinload

from core.crud import CRUDPaginated
from models.publishers import Author

author_crud = CRUDPaginated(
    model=Author,
)

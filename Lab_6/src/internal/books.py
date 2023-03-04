from core.crud import CRUDPaginated
from models.publishers import Book

book_crud = CRUDPaginated(model=Book)

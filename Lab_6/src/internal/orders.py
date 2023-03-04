from sqlalchemy.orm import joinedload

from core.crud import CRUDPaginated
from models.publishers import Order

order_crud = CRUDPaginated(
    model=Order,
    get_options=[joinedload(Order.book), joinedload(Order.customer)]
)
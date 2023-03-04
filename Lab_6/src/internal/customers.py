from core.crud import CRUDPaginated
from models.publishers import Customer

customer_crud = CRUDPaginated(
    model=Customer,
    # get_options=[joinedload(Customer.user)],
    # get_multi_options=[joinedload(Customer.user)]
)

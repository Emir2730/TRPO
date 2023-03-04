from core.crud import CRUDPaginated
from models.general import User

user_crud = CRUDPaginated(model=User)

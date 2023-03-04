from models.core import BaseModel, Base
from sqlalchemy import String, Column


class User(BaseModel, Base):
    __repr_name__ = 'Пользователь системы'
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    first_name: str = Column(String(256), nullable=False, comment='Имя')
    last_name: str = Column(String(256), nullable=False, comment='Фамилия')
    middle_name: str = Column(String(256), nullable=False, comment='Отчество')

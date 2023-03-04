"""
Стартовая настройка для sqlalchemy
"""
import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# metadata: MetaData = Base.metadata
# metadata.naming_convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }


def fresh_timestamp():
    """Небольшой хелпер для работы с timestamp на уровне ОРМа
    по сути "передает команду БД использовать нативную функцию NOW()"

    :return: [description]
    :rtype:
    """
    return datetime.datetime.utcnow()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"<{type(self).__name__}(id={self.id})>"


class TimestampMixin(object):
    created_at = Column(DateTime, default=fresh_timestamp())
    updated_at = Column(DateTime, default=fresh_timestamp(), onupdate=fresh_timestamp())
    deleted_at = Column(DateTime)

import datetime
import decimal

from sqlalchemy import Column, String, Text, ForeignKey, Integer, Boolean, DateTime, Float, Date
from sqlalchemy.orm import relationship

from models.core import BaseModel, Base, fresh_timestamp


class Author(BaseModel, Base):
    __repr_name__ = 'Писатель'
    __tablename__ = 'authors'
    __table_args__ = {'extend_existing': True}

    passport: str = Column(String(256), nullable=False, comment='Номер паспорта')
    address: str = Column(Text, nullable=False, comment='Домашний адрес')
    phone: str = Column(String(256), nullable=False, comment='Телефон')

    user_id: int = Column(ForeignKey('users.id'), nullable=False)

    # user: User = relationship('User', uselist=False)
    # contract: 'Contract' = relationship('Contract', uselist=False)
    # books: List['Book'] = relationship('Book', uselist=True)


class Contract(BaseModel, Base):
    __repr_name__ = 'Контракт с автором'
    __tablename__ = 'contracts'
    __table_args__ = {'extend_existing': True}

    number: int = Column(Integer, nullable=False, comment='Номер контракта')
    signing_date: datetime.datetime = Column(DateTime, nullable=False)
    term: int = Column(Integer, nullable=False, comment='Срок контракта')
    is_terminate: bool = Column(Boolean, server_default='false', comment='Расторгнут ли контракт')
    terminate_date: datetime.datetime = Column(DateTime, nullable=True, comment='Дата расторжения контракта')

    author_id: int = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author: Author = relationship('Author', uselist=False)


class Book(BaseModel, Base):
    __repr_name__ = 'Книга'
    __tablename__ = 'books'
    __table_args__ = {'extend_existing': True}

    name: str = Column(Text, nullable=False, comment='Название книги')
    isbn: str = Column(Text, nullable=False, comment='Шифр книг')
    edition: int = Column(Integer, nullable=False, comment='Тираж')
    expenses: decimal.Decimal = Column(Float, nullable=False, comment='Себестоимость')
    publication_date: datetime.date = Column(Date, nullable=False, comment='Дата выхода из печати')
    price: decimal.Decimal = Column(Float, nullable=False, comment='Цена продажи')
    total_royalti: decimal.Decimal = Column(Float, nullable=False, comment='Гонорар (на всех авторов книги)')

    # authors: List[Author] = relationship('Author', uselist=True)
    # orders: List['Order'] = relationship('Order', uselist=True)


class AuthorBook(BaseModel, Base):
    __repr_name__ = 'Автор книги'
    __tablename__ = 'book_authors'
    __table_args__ = {'extend_existing': True}

    author_id: int = Column(Integer, ForeignKey('authors.id'), nullable=False)
    book_id: int = Column(Integer, ForeignKey('books.id'), nullable=False)

    author: Author = relationship('Author', uselist=False)
    book: Book = relationship('Book', uselist=False)


class Customer(BaseModel, Base):
    __repr_name__ = 'Заказчик'
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}

    name: str = Column(String(512), nullable=False, comment='Название заказчика')
    address: str = Column(Text, nullable=False, comment='Адрес заказчика')
    phone: str = Column(String(128), nullable=False, comment='Телефон заказчика')

    user_id: int = Column(ForeignKey('users.id'), nullable=False, comment='Контактное лицо')

    # user: User = relationship('User', uselist=False)


class Order(BaseModel, Base):
    __repr_name__ = 'Заказ'
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}

    identifier: int = Column(Integer, nullable=False, comment='Номер заказа')
    book_id: int = Column(Integer, ForeignKey('books.id'), nullable=False)
    customer_id: int = Column(Integer, ForeignKey('customers.id'), nullable=False)

    created_at: datetime.datetime = Column(
        DateTime,
        nullable=False,
        on_create=fresh_timestamp(),
        comment='Дата поступления заказ в том числе'
    )
    closed_at: datetime.datetime = Column(DateTime, nullable=True, comment='Дата выполнения заказа')
    count: int = Column(Integer, nullable=False, comment='Количество экземпляров заказываемой книги')

    book: Book = relationship('Book', uselist=False)
    customer: Customer = relationship('Customer', uselist=False)

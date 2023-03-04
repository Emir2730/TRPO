import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.books import book_crud
from schemas.books import BookList, BookBare, BookFull, BookCreate, BookUpdate

books = fastapi.APIRouter()


@books.get('', response_model=BookList)
async def get_books(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> BookList:
    """
    Получение всех книг, доступных в системе
    """
    values, count = book_crud.get_multi(session, page, rows_per_page)

    data = [BookBare.from_orm(i) for i in values]
    return BookList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@books.get('/{book_id}', response_model=BookFull)
async def get_book(
        book_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> BookFull:
    """
    Получение информации о конкретной книге
    """
    book = book_crud.get(session, book_id)
    return BookFull.from_orm(book)


@books.post('', response_model=BookFull, status_code=201)
async def create_book(
        data: BookCreate,
        session: Session = fastapi.Depends(db_session),
) -> BookFull:
    """
    Создание новой книги
    """
    book = book_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
    )

    return BookFull.from_orm(book)


@books.put('/{book_id}', response_model=BookFull)
async def update_book(
        data: BookUpdate,
        book_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> BookFull:
    """
    Обновление информации о книге
    """
    book = book_crud.get(session, book_id)

    book = book_crud.update(
        session,
        book,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return BookFull.from_orm(book)


@books.delete('/{book_id}', response_model=BookFull)
async def delete_book(
        book_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> BookFull:
    """
    Удаление книги
    """
    book = book_crud.delete(session, id=book_id)
    return BookFull.from_orm(book)

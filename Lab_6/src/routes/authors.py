import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.authors import author_crud
from schemas.authors import AuthorList, AuthorBare, AuthorFull, AuthorCreate, AuthorUpdate

authors = fastapi.APIRouter()


@authors.get('', response_model=AuthorList)
async def get_authors(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> AuthorList:
    """
    Получение всех авторов, доступных в системе
    """
    values, count = author_crud.get_multi(session, page, rows_per_page)

    data = [AuthorBare.from_orm(i) for i in values]
    return AuthorList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@authors.get('/{author_id}', response_model=AuthorFull)
async def get_author(
        author_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> AuthorFull:
    """
    Получение информации о конкретном авторе
    """
    author = author_crud.get(session, author_id)
    return AuthorFull.from_orm(author)


@authors.post('', response_model=AuthorFull, status_code=201)
async def create_author(
        data: AuthorCreate,
        session: Session = fastapi.Depends(db_session),
) -> AuthorFull:
    """
    Создание нового автора
    """
    author = author_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
    )

    return AuthorFull.from_orm(author)


@authors.put('/{author_id}', response_model=AuthorFull)
async def update_author(
        data: AuthorUpdate,
        author_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> AuthorFull:
    """
    Обновление информации об авторе
    """
    author = author_crud.get(session, author_id)

    author = author_crud.update(
        session,
        author,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return AuthorFull.from_orm(author)


@authors.delete('/{author_id}', response_model=AuthorFull)
async def delete_author(
        author_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> AuthorFull:
    """
    Удаление автора
    """
    author = author_crud.delete(session, id=author_id)
    return AuthorFull.from_orm(author)

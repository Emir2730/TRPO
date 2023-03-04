import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.users import user_crud
from schemas.users import UserList, UserBare, UserFull, UserCreate, UserUpdate

users = fastapi.APIRouter()


@users.get('', response_model=UserList)
async def get_users(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> UserList:
    """
    Получение всех пользователей, доступных в системе
    """
    values, count = user_crud.get_multi(session, page, rows_per_page)

    data = [UserBare.from_orm(i) for i in values]
    return UserList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@users.get('/{user_id}', response_model=UserFull)
async def get_user(
        user_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> UserFull:
    """
    Получение информации о конкретном пользователе
    """
    user = user_crud.get(session, user_id)
    return UserFull.from_orm(user)


@users.post('', response_model=UserFull, status_code=201)
async def create_user(
        data: UserCreate,
        session: Session = fastapi.Depends(db_session),
) -> UserFull:
    """
    Создание нового пользователя
    """
    user = user_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
    )

    return UserFull.from_orm(user)


@users.put('/{user_id}', response_model=UserFull)
async def update_user(
        data: UserUpdate,
        user_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> UserFull:
    """
    Обновление информации о пользователе
    """
    user = user_crud.get(session, user_id)

    user = user_crud.update(
        session,
        user,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return UserFull.from_orm(user)


@users.delete('/{user_id}', response_model=UserFull)
async def delete_user(
        user_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> UserFull:
    """
    Удаление пользователя
    """
    user = user_crud.delete(session, id=user_id)
    return UserFull.from_orm(user)

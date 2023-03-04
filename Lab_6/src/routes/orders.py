import datetime

import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.orders import order_crud
from schemas.orders import OrderList, OrderBare, OrderFull, OrderCreate, OrderUpdate

orders = fastapi.APIRouter()


@orders.get('', response_model=OrderList)
async def get_orders(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> OrderList:
    """
    Получение всех пользователей, доступных в системе
    """
    values, count = order_crud.get_multi(session, page, rows_per_page)

    data = [OrderBare.from_orm(i) for i in values]
    return OrderList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@orders.get('/{order_id}', response_model=OrderFull)
async def get_order(
        order_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> OrderFull:
    """
    Получение информации о конкретном пользователе
    """
    order = order_crud.get(session, order_id)
    return OrderFull.from_orm(order)


@orders.post('', response_model=OrderFull, status_code=201)
async def create_order(
        data: OrderCreate,
        session: Session = fastapi.Depends(db_session),
) -> OrderFull:
    """
    Создание нового пользователя
    """
    order = order_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
        created_at=datetime.datetime.utcnow()
    )

    return OrderFull.from_orm(order)


@orders.put('/{order_id}', response_model=OrderFull)
async def update_order(
        data: OrderUpdate,
        order_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> OrderFull:
    """
    Обновление информации о пользователе
    """
    order = order_crud.get(session, order_id)

    order = order_crud.update(
        session,
        order,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return OrderFull.from_orm(order)


@orders.delete('/{order_id}', response_model=OrderFull)
async def delete_order(
        order_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> OrderFull:
    """
    Удаление пользователя
    """
    order = order_crud.delete(session, id=order_id)
    return OrderFull.from_orm(order)

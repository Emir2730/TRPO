import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.customers import customer_crud
from schemas.customers import CustomerList, CustomerBare, CustomerFull, CustomerCreate, CustomerUpdate

customers = fastapi.APIRouter()


@customers.get('', response_model=CustomerList)
async def get_customers(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> CustomerList:
    """
    Получение всех книг, доступных в системе
    """
    values, count = customer_crud.get_multi(session, page, rows_per_page)

    data = [CustomerBare.from_orm(i) for i in values]
    return CustomerList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@customers.get('/{customer_id}', response_model=CustomerFull)
async def get_customer(
        customer_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> CustomerFull:
    """
    Получение информации о конкретной книге
    """
    customer = customer_crud.get(session, customer_id)
    return CustomerFull.from_orm(customer)


@customers.post('', response_model=CustomerFull, status_code=201)
async def create_customer(
        data: CustomerCreate,
        session: Session = fastapi.Depends(db_session),
) -> CustomerFull:
    """
    Создание новой книги
    """
    customer = customer_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
    )

    return CustomerFull.from_orm(customer)


@customers.put('/{customer_id}', response_model=CustomerFull)
async def update_customer(
        data: CustomerUpdate,
        customer_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> CustomerFull:
    """
    Обновление информации о книге
    """
    customer = customer_crud.get(session, customer_id)

    customer = customer_crud.update(
        session,
        customer,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return CustomerFull.from_orm(customer)


@customers.delete('/{customer_id}', response_model=CustomerFull)
async def delete_customer(
        customer_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> CustomerFull:
    """
    Удаление книги
    """
    customer = customer_crud.delete(session, id=customer_id)
    return CustomerFull.from_orm(customer)

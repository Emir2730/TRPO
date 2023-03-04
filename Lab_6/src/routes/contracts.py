import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.crud import ExcludePolicyEnum
from dependencies.db import db_session
from internal.contracts import contract_crud
from schemas.contracts import ContractList, ContractBare, ContractFull, ContractCreate, ContractUpdate

contracts = fastapi.APIRouter()


@contracts.get('', response_model=ContractList)
async def get_contracts(
        session: Session = fastapi.Depends(db_session),
        page: int = fastapi.Query(1, alias='page'),
        rows_per_page: int = fastapi.Query(25, alias='rowsPerPage', le=101),
) -> ContractList:
    """
    Получение всех пользователей, доступных в системе
    """
    values, count = contract_crud.get_multi(session, page, rows_per_page)

    data = [ContractBare.from_orm(i) for i in values]
    return ContractList(
        data=data, rows_per_page=rows_per_page,
        page=page, rows_number=count
    )


@contracts.get('/{contract_id}', response_model=ContractFull)
async def get_contract(
        contract_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> ContractFull:
    """
    Получение информации о конкретном пользователе
    """
    contract = contract_crud.get(session, contract_id)
    return ContractFull.from_orm(contract)


@contracts.post('', response_model=ContractFull, status_code=201)
async def create_contract(
        data: ContractCreate,
        session: Session = fastapi.Depends(db_session),
) -> ContractFull:
    """
    Создание нового пользователя
    """
    contract = contract_crud.create(
        session,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset,
    )

    return ContractFull.from_orm(contract)


@contracts.put('/{contract_id}', response_model=ContractFull)
async def update_contract(
        data: ContractUpdate,
        contract_id: int = fastapi.Path(..., ge=1),
        session: Session = fastapi.Depends(db_session),
) -> ContractFull:
    """
    Обновление информации о пользователе
    """
    contract = contract_crud.get(session, contract_id)

    contract = contract_crud.update(
        session,
        contract,
        data,
        cast_policy=ExcludePolicyEnum.exclude_unset
    )
    return ContractFull.from_orm(contract)


@contracts.delete('/{contract_id}', response_model=ContractFull)
async def delete_contract(
        contract_id: int = fastapi.Path(..., ge=1),
        session: AsyncSession = fastapi.Depends(db_session),
) -> ContractFull:
    """
    Удаление пользователя
    """
    contract = contract_crud.delete(session, id=contract_id)
    return ContractFull.from_orm(contract)

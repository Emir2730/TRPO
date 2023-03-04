from http import HTTPStatus
from typing import TypeVar, Type, Union, Optional, List, Tuple

import fastapi
from sqlalchemy.orm import Query

from models.core import Base

RetrieveType = TypeVar('RetrieveType', bound=Base)


def retrieve_object(
        query: Query,
        model: Type[RetrieveType],
        id: Union[int, str],
        raise_deleted: bool = False
) -> RetrieveType:
    """
    Запрашивает требуемый объект по идентификатору.

    При отсутствии объекта в бд, вызывает ошибку
    :param query: запрос, по которому будет получен объект
    :param model: класс запрашиваемого объекта
    :param id: идентификатор объекта в бд
    :param raise_deleted: выдавать ошибки для удалённых значений (по полю deleted_at)
    :raises ObjectNotExists
    """

    obj = query.filter(model.id == id).first()
    if obj is None:
        raise fastapi.HTTPException(HTTPStatus.NOT_FOUND, 'Объект не найден')

    if raise_deleted and getattr(obj, 'deleted_at', None):
        raise fastapi.HTTPException(HTTPStatus.NOT_FOUND, 'Объект не найден')

    return obj


SearchType = TypeVar('SearchType', bound=Base)
Count = int


def pagination(
        query: Query,
        page: int = 1,
        rows_per_page: Optional[int] = 25,
        ModelClass: Type[SearchType] = Base,
        with_count: bool = True,
        with_deleted: bool = False,
        hide_deleted: bool = False
) -> Tuple[List[SearchType], Count]:
    """
    Выполняет запрос с пагинацией.

    Явно указывать запрос им
    :param query: запрос по которому будет выполнен запрос
    :param page: страница
    :param rows_per_page: кол-во элементов на 1 странице выдачи
    :param hide_deleted: параметр явно фильтрующий по deleted_at
    :param ModelClass: класс для возвращаемых значений. Нужен для typehints
    :return: Список значений и предельное их кол-во
    """
    if with_deleted:
        query = query.execution_options(include_deleted=True)

    if hide_deleted:
        # noinspection PyComparisonWithNone
        query = query.filter(ModelClass.deleted_at == None)

    rows_number = query.count() if with_count else None

    if rows_per_page:
        query = query.limit(rows_per_page)

    final_query = query.offset((page - 1) * (rows_per_page or 0))
    return final_query.all(), rows_number

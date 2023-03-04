from typing import TypeVar, List, Optional, Type, Any

import pydantic
from sqlalchemy.ext.asyncio import AsyncSession


def to_camel(string: str) -> str:
    """
    Верблюдезирует строку, со строчным написанием первого слова

    to_camel_case -> toCamelCase

    :param string: строка в snake case'е
    :type string: str
    :return: строка в camel case'е
    :rtype: str
    """
    return ''.join(word if i == 0 else word.capitalize() for i, word in enumerate(string.split('_')))


class Model(pydantic.BaseModel):
    """
    Промежуточная модель pydantic'а для унифицирования конфигов и удобного администрирования
    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

    # noinspection Pydantic
    @classmethod
    async def from_orm_async(cls: Type['Model'], obj: Any, session: AsyncSession) -> 'Model':
        """
        При запросе ORM моделей, с помощью асинхронной сессии, невозможно
        подгрузить отношения в асинхронном контексте "on-demand" (lazy-load при запросе вложенной сущности).
        Также, могут возникнуть проблемы для полей, с ``server_default`` параметрами.

        В связи с вышеперечисленными проблемами есть 2 варианта сериализации ORM модели к Pydantic схеме:
         * использование классического (синхронного метода ``from_orm``) с предварительной подгрузкой всех сущностей
         * использование асинхронного ``from_orm_async``

        При первом сценарии, необходимо, чтобы все маппящиеся свойства были предварительно подгружены,
        для этого можно использовать метод ``session.refresh(<entity_var>, (*<field_name>))``
        (работает и для ``server_default`` и для вложенных сущностей).
        Либо при составлении запроса, указывать все вложенные сущности, с помощью метода запроса ``options``,
        например, ``select(User).options(joinedload(Role))``.

        **также, необходимо помнить, что для полей ORM модели с параметром ``server_default``, работает
        стандартное правило ``expire_on_commit``**
        (правда мы не используем ``session.commit()`` явно, за редкими исключениями, но всё же)
        """
        mapper = lambda sess, obj: cls.from_orm(obj)
        return await session.run_sync(mapper, obj)


ListElement = TypeVar('ListElement', bound=Model)


class ListModel(Model):
    """
    Формат выдачи для всех списков объектов (multiple get)
    """
    rows_per_page: Optional[int]
    page: Optional[int]
    rows_number: Optional[int]
    show_deleted: bool = False
    data: List[ListElement]
    sort_by: str = 'id'


class StatusResponse(pydantic.BaseModel):
    """
    Формат ответа для запросов, в которых не требуется отдавать данные
    """
    status: str = 'ok'
    warning: Optional[str] = None
    warning_info: List[dict] = pydantic.Field(default_factory=list)

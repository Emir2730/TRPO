"""init

Create Date: 2022-12-15 18:05:00.756486

"""
from models import User

revision = ('13feee3e626c',)

from typing import Tuple

import sqlalchemy as sa


# Please, write your values here
def data_upgrade(op):
    connection: sa.engine.Connection = op.get_bind()


def data_downgrade(op):
    connection: sa.engine.Connection = op.get_bind()

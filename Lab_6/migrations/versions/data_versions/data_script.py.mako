"""${message}

Create Date: ${create_date}

"""

revision = ${revision}

from typing import Tuple

import sqlalchemy as sa


def data_upgrade(op):
    connection: sa.engine.Connection = op.get_bind()


def data_downgrade(op):
    connection: sa.engine.Connection = op.get_bind()

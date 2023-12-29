from sqlalchemy import Table, Column
from sqlalchemy import INT, VARCHAR

from sqlalchemy.orm import registry
from .. import mapping_assembler

from data_lib.model.entities import Subject


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_Subject(__reg: registry):
    """Maps `Subject` class onto the `subjects` table."""

    __reg.map_imperatively(
        Subject,
        Table(
            'subjects',
            __reg.metadata,

            Column('subject_id', INT, primary_key=True, key='id'),

            Column('subject_code', VARCHAR(64), nullable=False, unique=True, key='code'),
            Column('subject_name', VARCHAR, nullable=True, key='name')
        )
    )

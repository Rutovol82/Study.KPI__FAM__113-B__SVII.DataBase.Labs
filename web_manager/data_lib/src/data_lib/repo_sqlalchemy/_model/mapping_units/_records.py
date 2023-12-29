from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT, CHAR

from sqlalchemy.orm import registry
from .. import mapping_assembler

from data_lib.model.entities import Record


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_Record(__reg: registry):
    """Maps `Record` class onto the `records` table."""

    __reg.map_imperatively(
        Record,
        Table(
            'records',
            __reg.metadata,

            Column('record_id', CHAR(36), primary_key=True, key='id'),

            Column('record_year', INT),
            Column('examinee_id', INT, ForeignKey('examinees_data.id'), nullable=True)
        )
    )

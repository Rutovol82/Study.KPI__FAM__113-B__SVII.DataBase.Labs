from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT, VARCHAR

from sqlalchemy.orm import registry
from ... import mapping_assembler

from data_lib.model.entities import TestPoint


# Define public visible members
__all__ = ['map_TestPoint']


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_TestPoint(__reg: registry):
    """Maps `TestPoint` class onto the `test_points` table."""

    __reg.map_imperatively(
        TestPoint,
        Table(
            'test_points',
            __reg.metadata,

            Column('point_id', INT, primary_key=True, key='id'),

            Column('point_name', VARCHAR, key='name'),
            Column('location_terr_id', INT, ForeignKey("territories.id"), nullable=True)
        )
    )

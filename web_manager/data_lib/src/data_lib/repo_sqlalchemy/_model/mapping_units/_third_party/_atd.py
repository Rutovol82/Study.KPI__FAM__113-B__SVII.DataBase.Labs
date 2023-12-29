from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT, VARCHAR

from sqlalchemy.orm import registry
from ... import mapping_assembler

from data_lib.model.entities import Region, Area, Territory


# Define public visible members
__all__ = ['map_Region', 'map_Area', 'map_Territory']


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_Region(__reg: registry):
    """Maps `Region` class onto the `regions` table."""

    __reg.map_imperatively(
        Region,
        Table(
            'regions',
            __reg.metadata,

            Column('region_id', INT, primary_key=True, key='id'),

            Column('region_name', VARCHAR, key='name')
        )
    )


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_Area(__reg: registry):
    """Maps `Area` class onto the `areas` table."""

    __reg.map_imperatively(
        Area,
        Table(
            'areas',
            __reg.metadata,

            Column('area_id', INT, primary_key=True, key='id'),

            Column('region_id', INT, ForeignKey("regions.id")),
            Column('area_name', VARCHAR, key='name')
        )
    )


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_Territory(__reg: registry):
    """Maps `Territory` class onto the `territories` table."""

    __reg.map_imperatively(
        Territory,
        Table(
            'territories',
            __reg.metadata,

            Column('terr_id', INT, primary_key=True, key='id'),

            Column('area_id', INT, ForeignKey("areas.id")),
            Column('terr_name', VARCHAR, key='name')
        )
    )

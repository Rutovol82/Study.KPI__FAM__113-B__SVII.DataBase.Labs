from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT, VARCHAR

from sqlalchemy.orm import registry
from ... import mapping_assembler

from data_lib.model.entities import EduOrgType, EduSupervisor, EduOrganization


# Define public visible members
__all__ = ['map_EduOrgType', 'map_EduSupervisor', 'map_EduOrganization']


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_EduOrgType(__reg: registry):
    """Maps `EduOrgType` class onto the `edu_orgtypes` table."""

    __reg.map_imperatively(
        EduOrgType,
        Table(
            'edu_orgtypes',
            __reg.metadata,

            Column('type_id', INT, primary_key=True, key='id'),

            Column('type_name', VARCHAR, key='name')
        )
    )


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_EduSupervisor(__reg: registry):
    """Maps `EduSupervisor` class onto the `edu_supers` table."""

    __reg.map_imperatively(
        EduSupervisor,
        Table(
            'edu_supers',
            __reg.metadata,

            Column('super_id', INT, primary_key=True, key='id'),

            Column('super_name', VARCHAR, key='name')
        )
    )


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_EduOrganization(__reg: registry):
    """Maps `EduOrganization` class onto the `edu_orgs` table."""

    __reg.map_imperatively(
        EduOrganization,
        Table(
            'edu_orgs',
            __reg.metadata,

            Column('org_id', INT, primary_key=True, key='id'),

            Column('org_name', VARCHAR, key='name'),
            Column('location_terr_id', INT, ForeignKey("territories.id"), nullable=True),
            Column('orgtype_id', INT, ForeignKey("edu_orgtypes.id"), nullable=True, key='type_id'),
            Column('super_id', INT, ForeignKey("edu_supers.id"), nullable=True)
        )
    )

from sqlalchemy import Table, Column
from sqlalchemy import INT, VARCHAR

from sqlalchemy.orm import registry
from ... import mapping_assembler

from data_lib.model.entities import EduLang, EduProfile


# Define public visible members
__all__ = ['map_EduLang', 'map_EduProfile']


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_EduLang(__reg: registry):
    """Maps `EduLang` class onto the `edu_langs` table."""

    __reg.map_imperatively(
        EduLang,
        Table(
            'edu_langs',
            __reg.metadata,

            Column('lang_id', INT, primary_key=True, key='id'),

            Column('lang_name', VARCHAR, key='name')
        )
    )


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_EduProfile(__reg: registry):
    """Maps `EduProfile` class onto the `edu_profiles` table."""

    __reg.map_imperatively(
        EduProfile,
        Table(
            'edu_profiles',
            __reg.metadata,

            Column('profile_id', INT, primary_key=True, key='id'),

            Column('profile_name', VARCHAR, key='name')
        )
    )

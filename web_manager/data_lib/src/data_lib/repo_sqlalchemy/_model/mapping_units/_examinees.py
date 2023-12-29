from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT

from sqlalchemy.orm import registry
from .. import mapping_assembler

from data_lib.model.entities import ExamineeData
from ..types import sex, terrtype, edu_status


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_ExamineeData(__reg: registry):
    """Maps `ExamineeData` class onto the `examinees_data` table."""

    __reg.map_imperatively(
        ExamineeData,
        Table(
            'examinees_data',
            __reg.metadata,

            Column('examinee_id', INT, primary_key=True, key='id'),

            Column('sex', sex(), nullable=True),
            Column('birth_year', INT, nullable=True),

            Column('residence_terr_id', INT, ForeignKey("territories.id"), nullable=True),
            Column('residence_terrtype', terrtype(), nullable=True),

            Column('edu_profile_id', INT, ForeignKey('edu_profiles.id'), nullable=True),
            Column('edu_lang_id', INT, ForeignKey('edu_langs.id'), nullable=True),

            Column('edu_org_id', INT, ForeignKey('edu_orgs.id'), nullable=True),
            Column('edu_status', edu_status(), nullable=True)
        )
    )

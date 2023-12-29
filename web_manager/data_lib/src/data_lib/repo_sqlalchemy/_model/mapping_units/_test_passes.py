from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import INT, DECIMAL, CHAR

from sqlalchemy.orm import registry
from .. import mapping_assembler

from data_lib.model.entities import TestPass
from ..types import test_status, dpa_level


# noinspection PyPep8Naming
@mapping_assembler.register_unit
def map_TestPass(__reg: registry):
    """Maps `TestPass` class onto the `test_passes` table."""

    __reg.map_imperatively(
        TestPass,
        Table(
            'test_passes',
            __reg.metadata,

            Column('pass_id', INT, primary_key=True, key='id'),

            Column('record_id', CHAR(36), ForeignKey("records.id"), nullable=False),
            Column('subject_id', INT, ForeignKey("subjects.id"), nullable=False),

            Column('test_status', INT, test_status(), nullable=False),
            Column('super_pass_id', INT, ForeignKey("test_passes.id"), nullable=True),

            Column('test_point_id', INT, ForeignKey('test_points.id'), nullable=True),

            Column('test_lang_id', INT, ForeignKey('edu_langs.id'), nullable=True),
            Column('adapt_scale', INT, nullable=True),
            Column('dpa_level', dpa_level(), nullable=True),

            Column('score', INT, nullable=True),
            Column('score_12', INT, nullable=True),
            Column('score_100', DECIMAL, nullable=True),
        )
    )

import enum

from sqlalchemy import Enum

from functools import partial

from data_lib.model.types import Sex, EduStatus, TerrType, DPALevel, TestStatus


# Define public visible members
__all__ = ['sex', 'edu_status', 'terrtype', 'dpa_level', 'test_status']


# Define unified function to be passed to `SQLAlchemy` `Enum` as `values_callable` argument
def _extract_enum_values(__enum: enum.Enum) -> list:
    """Function, provides extraction of the passed enum values as the list."""

    # noinspection PyTypeChecker
    return [e_.value for e_ in __enum]


# ------ Define `SQLAlchemy` enum types mapping

sex = partial(Enum, Sex, name='sex', values_callable=_extract_enum_values)
"""Enumeration represents **DPA level**."""

edu_status = partial(Enum, EduStatus, name='edu_status', values_callable=_extract_enum_values)
"""Enumeration represents **educational status**."""

terrtype = partial(Enum, TerrType, name='terrtype', values_callable=_extract_enum_values)
"""Enumeration represents examinee **residence territory type**."""

dpa_level = partial(Enum, DPALevel, name='dpa_level', values_callable=_extract_enum_values)
"""Enumeration represents **DPA level**."""

test_status = partial(Enum, TestStatus, name='test_status', values_callable=_extract_enum_values)
"""Enumeration represents **test pass status**."""

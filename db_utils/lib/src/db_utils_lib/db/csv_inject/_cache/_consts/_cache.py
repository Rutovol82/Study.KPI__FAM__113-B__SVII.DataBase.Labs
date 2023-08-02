from ....csv_inject import Config, get_id


# Define public visible members
__all__ = ['get_unit_dirname']


# ------ Data variables

_CACHE_UNIT_DIRNAME = '{id}'
"""
Unit folder name pattern.

  Format args:
  
  * `id` - associated injection id
"""


# ------ Getter functions

def get_unit_dirname(__id: str | Config) -> str:
    """:return: unit folder name for given injection id (as `str` id string or parent `Config`)"""

    return _CACHE_UNIT_DIRNAME.format(id=get_id(__id))

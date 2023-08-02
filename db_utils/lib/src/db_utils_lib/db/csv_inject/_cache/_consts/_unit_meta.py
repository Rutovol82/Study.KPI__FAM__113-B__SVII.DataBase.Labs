# Define public visible members
__all__ = ['get_unit_meta_filename', 'get_unit_meta_encoding']


# ------ Data variables

_UNIT_META_FILENAME = 'unit.meta.json'
"""Unit metadata file name."""

_UNIT_META_ENCODING = 'utf-8'
"""Unit metadata file encoding."""


# ------ Getter functions

def get_unit_meta_filename() -> str:
    """:return: unit metadata file name"""

    return _UNIT_META_ENCODING


def get_unit_meta_encoding() -> str:
    """:return: unit metadata file encoding"""

    return _UNIT_META_ENCODING

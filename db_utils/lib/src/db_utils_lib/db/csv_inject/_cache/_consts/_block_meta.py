# Define public visible members
__all__ = ['get_block_meta_filename', 'get_block_meta_encoding']


# ------ Data variables

_BLOCK_META_FILENAME = '{block_num}.block.meta.json'  # Cached data block metadata file name
"""
Cached data block metadata file name formatting pattern.

  Format args:

  * `block_num` - data block number
"""

_BLOCK_META_ENCODING = 'utf-8'
"""Cached data block metadata file encoding."""


# ------ Getter functions

def get_block_meta_filename(block_num: int) -> str:
    """:return: cached data block metadata file name for given block number (`block_num`)"""

    return _BLOCK_META_FILENAME.format(block_num=block_num)


def get_block_meta_encoding() -> str:
    """:return: cached data block metadata file encoding"""

    return _BLOCK_META_ENCODING

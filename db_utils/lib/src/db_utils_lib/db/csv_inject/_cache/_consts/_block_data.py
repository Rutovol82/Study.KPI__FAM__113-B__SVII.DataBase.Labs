from db_utils_lib.std_utils import Parameterizable, FrozenParams


# Define public visible members
__all__ = ['get_block_data_filename', 'get_block_data_encoding', 'get_block_data_csv_opts']


# ------ Data variables

_BLOCK_DATA_FILENAME = '{block_num}.block.csv'
"""
Cached data block data file name formatting pattern.

  Format args:

  * `block_num` - data block number
"""

_BLOCK_DATA_ENCODING = 'utf-8'
"""Cached data block data file encoding."""

_BLOCK_DATA_CSV_OPTS = FrozenParams()
"""Cached data block data file `csv` options."""


# ------ Getter functions

def get_block_data_filename(block_num: int) -> str:
    """:return: cached data block data file name for given block number (`block_num`)"""

    return _BLOCK_DATA_FILENAME.format(block_num=block_num)


def get_block_data_encoding() -> str:
    """:return: cached data block data file encoding"""

    return _BLOCK_DATA_ENCODING


def get_block_data_csv_opts() -> Parameterizable:
    """:return: cached data block data file `csv` options to be passed to readers/writers from `csv` module"""

    return _BLOCK_DATA_CSV_OPTS

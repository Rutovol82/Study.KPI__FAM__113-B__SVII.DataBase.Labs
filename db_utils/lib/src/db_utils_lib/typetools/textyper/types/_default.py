import re

from .. import TexType


# Define public visible members
__all__ = ['INT', 'FLOAT', 'STR']


# ------ Define integer textype

INT_MATCH = re.compile(r'^\s*(\d+)\s*$')
# noinspection PyTypeChecker
INT = TexType(
    key_='int', type_=int,
    load_func=int, dump_func=str,
    match_func=lambda s: re.fullmatch(INT_MATCH, s) is not None
)
"""`TexTypeABC` instance for the textype corresponds Python `int`."""


# ------ Define float textype

FLOAT_MATCH = re.compile(r'^\s*(\d+.\d+)\s*$')
# noinspection PyTypeChecker
FLOAT = TexType(
    key_='float', type_=float,
    load_func=float, dump_func=str,
    match_func=lambda s: re.fullmatch(FLOAT_MATCH, s) is not None
)
"""`TexTypeABC` instance for the textype corresponds Python `float`."""


# ------ Define string textype

STR = TexType(
    key_='str', type_=str,
    load_func=lambda x: x, dump_func=lambda x: x,
    match_func=lambda _: True
)
"""`TexTypeABC` instance for the textype corresponds Python `str`."""

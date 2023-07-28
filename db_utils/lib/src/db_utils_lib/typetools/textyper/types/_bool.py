import re

from db_utils_lib.std_helpers import Singleton

from .. import TexTypeABC


# Define public visible members
__all__ = ['BooleanTexType', 'BOOL']


class BooleanTexType(TexTypeABC, Singleton):
    """`TexTypeABC` implementation for the textype corresponds Python `bool`."""

    _KEY: str = 'bool'  # Typekey value

    _TRUE_MATCH: re.Pattern = re.compile(r'(?i)^TRUE$')     # `True` value match regex pattern
    _FALSE_MATCH: re.Pattern = re.compile(r'(?i)^FALSE$')   # `False` value match regex pattern

    _TRUE_STRING: str = 'true'      # `True` value corresponding string
    _FALSE_STRING: str = 'false'    # `False` value corresponding string

    @property
    def key(self) -> str:
        return self._KEY

    @property
    def type(self) -> type:
        return bool

    def load(self, str_: str) -> bool:

        # Check for `True` match
        if self._TRUE_MATCH.match(str_):
            return True

        # Check for `False` match
        if self._FALSE_MATCH.match(str_):
            return False

        # Raise `ValueError`
        raise ValueError(f"'{str_}' can not be recognized as bool.")

    def dump(self, val_: bool) -> str:
        return self._TRUE_STRING if val_ else self._FALSE_STRING

    def match(self, str_: str) -> bool:
        return self._TRUE_MATCH.match(str_) is not None or self._FALSE_MATCH.match(str_) is not None


BOOL = BooleanTexType()
"""`TexTypeABC` instance for the textype corresponds Python `bool`."""

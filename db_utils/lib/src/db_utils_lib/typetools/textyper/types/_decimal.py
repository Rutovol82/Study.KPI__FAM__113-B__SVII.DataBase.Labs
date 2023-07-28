import re
import decimal

from db_utils_lib.std_helpers import Singleton

from .. import TexTypeABC


# Define public visible members
__all__ = ['DecimalTexType', 'DECIMAL']


class DecimalTexType(TexTypeABC, Singleton):
    """`TexTypeABC` implementation for the textype corresponds Python `decimal.Decimal`."""

    _KEY: str = 'decimal'  # Typekey value
    _MATCH: re.Pattern = re.compile(r'^\s*(\d+(.\d+)?)\s*$')  # Match regex pattern

    @property
    def key(self) -> str:
        return self._KEY

    @property
    def type(self) -> type:
        return decimal.Decimal

    def load(self, str_: str) -> decimal.Decimal:
        try:
            return decimal.Decimal(str_)
        except decimal.InvalidOperation as e:
            raise ValueError("Decimal conversion failed.") from e

    def dump(self, val_: decimal.Decimal) -> str:
        return str(val_)

    def match(self, str_: str) -> bool:
        return re.match(self._MATCH, str_) is not None


DECIMAL = DecimalTexType()
"""`TexTypeABC` instance for the textype corresponds Python `decimal.Decimal`."""

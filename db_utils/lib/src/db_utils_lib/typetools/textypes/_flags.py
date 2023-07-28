import re
from enum import IntFlag

from db_utils_lib.std_helpers import FlagGetterMixin


# Define public visible members
__all__ = ['Flags', 'NULL', 'SQUOTE', 'DQUOTE', 'QUOTE']


_KEY_FLAG_MATCH = re.compile(r'^\[(?P<flag>[a-z]+)]\s*')
"""Regex pattern, matches flag sequence in typekey."""


class Flags(FlagGetterMixin, IntFlag):
    """`textypes` flags used by `textypes.Handler`"""

    NULL = int('0b001', 2)
    """Flag specifies that textype supports `null` values."""

    SQUOTE = int('0b010', 2)
    """Flag specifies that textype value must be wrapped/unwrapped with single-quotes on dump/load."""

    DQUOTE = int('0b100', 2)
    """Flag specifies that textype value must be wrapped/unwrapped with double-quotes on dump/load."""

    QUOTE = SQUOTE | DQUOTE
    """
    Flag specifies that textype value must be wrapped double-quotes on dump 
    and unwrapped from single/double-quotes on load.
    """

    @classmethod
    def from_typekey(cls, key_: str):
        """
        Extracts `textypes.Flags` from typekey and normalizes typekey to type-only definition.

        :raise KeyError: if one of flags not found

        :rtype: tuple[int | Flags, str]
        :return: `textypes.Flags` (0 if flags not found), reduced typekey
        """

        flag_ = 0  # Initial flag

        while True:
            # Find flag definition sequence match
            match = re.match(_KEY_FLAG_MATCH, key_)

            # Exit if not found
            if match is None:
                break

            # Append resulting `flag_` & reduce `key_`
            flag_ |= cls[match.group('flag').upper()]
            key_ = re.sub(_KEY_FLAG_MATCH, '', key_)

        return flag_, key_


NULL = Flags.NULL
SQUOTE = Flags.SQUOTE
DQUOTE = Flags.DQUOTE
QUOTE = Flags.QUOTE

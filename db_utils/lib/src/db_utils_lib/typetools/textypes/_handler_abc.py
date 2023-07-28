from abc import abstractmethod, ABCMeta
from typing import Any, Literal

from . import Flags


class HandlerABC(metaclass=ABCMeta):
    """
    Abstraction helps manage string values types, their serialization and deserialization
    across storages supports only text storage without saving types.

      Helps associate type with string typekey,
      properly serialize & deserialize value by that key or associated type.
    """

    # ------ Abstract interface methods

    @abstractmethod
    def dump(self, val_: Any, type_or_key: str | type | Literal['auto'] = 'auto', flags: Flags | str = 0) -> str:
        """
        Serializes `val_` into string using stored protocols
        and optional `type_or_key` type specification (type or typekey).

        :raise KeyError: if typekey, passed by `type_or_key` was not found /
                         one of flags extracted from typekey not found
        :raise TypeError: if type, passed by `type_or_key` or get from `val_` is not supported
        :raise ValueError: if `val_` typekey not supports dump

        :param val_: value to be serialized
        :param type_or_key: `val_` typekey or type (if `'auto'` passed - will be taken from `val_`)
        :param flags: `textypes` flags, affects behavior (will be compiled with extracted from typekey if provided)

        :return: serialized string equivalent of `val_` value
        """

    @abstractmethod
    def load(self, str_: str, type_or_key: str | type | Literal['auto'] = 'auto', flags: Flags | str = 0) -> Any:
        """
        Serializes `val_` into string using stored protocols
        and optional `type_or_key` type specification (type or typekey).

        :raise KeyError: if typekey, passed by `type_or_key` was not found /
                         one of flags extracted from typekey not found
        :raise TypeError: if type, passed by `type_or_key` is not supported /
                          `None` or `NoneType` passed to `type_or_key` but `NULL` flag not provided
        :raise ValueError: if `type_or_key` not provided and `str_` typekey not recognized /
                           its typekey not supports load

        :param str_: value to be deserialized
        :param type_or_key: `val_` typekey or type (if `'auto'` passed - will be recognized from `str_`)
        :param flags: `textypes` flags, affects behavior (will be compiled with extracted from typekey if provided)

        :return: deserialized value of `str_`
        """

    @abstractmethod
    def get_key_type(self, key_: str) -> type:
        """
        Returns type corresponding passed typekey.

        **NOTE**: Returns `NoneType` for `None` typekey (matches `null` values).

        :raise KeyError: if typekey not found
        """

    @abstractmethod
    def get_type_key(self, type_: type) -> str | None:
        """
        Returns typekey corresponding passed type.

        **NOTE**: Returns `None` typekey for `NoneType` type or `None` value (matches `null` values).

        :raise TypeError: if type is not supported
        """

    @abstractmethod
    def get_str_type(self, str_: str, flags: Flags | str = 0) -> type:
        """
        Returns recognized `str_` type.

        **NOTE**: Returns `NoneType` type if `NULL` flag set and `str_` is `null`-string.

        :param str_: string value to recognize type from
        :param flags: `textypes` flags, affects behavior

        :raise ValueError: if `str_` type was not recognized
        """

    @abstractmethod
    def get_str_key(self, str_: str, flags: Flags | str = 0) -> str | None:
        """
        Returns recognized `str_` typekey.

        **NOTE**: Returns `None` typekey if `NULL` flag set and `str_` is `null`-string.

        :param str_: string value to recognize type from
        :param flags: `textypes` flags, affects behavior

        :raise ValueError: if `str_` typekey was not recognized
        """

    # ------ Protected static service methods

    @staticmethod
    def _resolve_flags(flags: Flags | str) -> Flags:
        """
        Little service method - helps to resolve multi-mode passed flags.

        Checks if `flags` is flags literal and extracts `textypes.Flags` from it.

        :return: normalized `textypes.Flags`
        """

        if type(flags) is str:
            return Flags.from_literal(flags)
        return flags

    @staticmethod
    def _resolve_load_quotes(str_: str, flags: Flags = 0) -> str:
        """
        Little service method - helps to handle quoting flags on loading string value.

        :return: normalized string value ready to load
        """

        # Unquote value if needed
        if len(str_) >= 2 and ((flags & Flags.DQUOTE and str_[0] == '"' and str_[-1] == '"') or
                               (flags & Flags.SQUOTE and str_[0] == "'" and str_[-1] == "'")):
            return str_[1:-1]

        return str_

    @staticmethod
    def _resolve_dump_quotes(str_: str, flags: Flags = 0) -> str:
        """
        Little service method - helps to handle quoting flags on dumping string value.

        :return: normalized string value ready to dump
        """

        if flags & Flags.DQUOTE:
            return '"' + str_ + '"'

        if flags & Flags.SQUOTE:
            return "'" + str_ + "'"

        return str_

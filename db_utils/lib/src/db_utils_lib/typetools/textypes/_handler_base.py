from abc import abstractmethod, ABCMeta
from collections.abc import Iterable, Sequence
from types import NoneType
from typing import Any, Literal

from . import Flags, HandlerABC


class HandlerBase(HandlerABC, metaclass=ABCMeta):
    """
    Additional `textypes.Handler` abstraction layer, implements some original functions for more suitable inheritance.
    """

    # ------ Protected static fields

    _DEFAULT_NULL_ALIAS: Sequence[str] = ('null',)   # Default value for `null_alias`

    # ------ Protected fields & public properties

    _null_alias: Sequence[str]  # Sequence of `null` value string alias. First value is default.

    @property
    def null_alias(self) -> Iterable[str]:
        """Iterable of `null` value string alias. First value is default."""
        return iter(self._null_alias)

    @property
    def null_string(self) -> str:
        """Default `null` string value."""
        return self._null_alias[0]

    # ------ Instantiation methods

    @abstractmethod
    def __init__(self, *, null_alias: Sequence[str] = None):
        """
        Abstract `HandlerBase` initialization method.

        :param null_alias: sequence of `null` value string alias - first value is default
        """

        self._null_alias = null_alias if null_alias is not None else self._DEFAULT_NULL_ALIAS

    # ------ Implemented functionality methods

    def load(self, str_: str, type_or_key: str | type | Literal['auto'] = 'auto', flags: Flags | str = 0) -> Any:

        flags: Flags = self._resolve_flags(flags)   # Handle input flags

        # Extract additional flags from typekey if provided & add to primary `flags`
        if type(type_or_key) is str and type_or_key != 'auto':
            key_flags, type_or_key = Flags.from_typekey(type_or_key)
            flags |= key_flags

        # Handle `null`-string
        if str_ in self._null_alias and flags & Flags.NULL:
            return None

        # Try to recognize string value typekey if `'auto'` passed to `type_or_key`
        if type_or_key == 'auto':
            type_or_key = self.get_str_key(str_)

        # Extract typekey from type if it supplied by `type_or_key`
        elif isinstance(type_or_key, type):
            type_or_key = self.get_type_key(type_or_key)

        return self._load_by_key(self._resolve_load_quotes(str_, flags), type_or_key)

    def dump(self, val_: Any, type_or_key: str | type | Literal['auto'] = 'auto', flags: Flags | str = 0) -> str:

        flags: Flags = self._resolve_flags(flags)  # Handle input flags

        # Extract additional flags from typekey if provided & add to primary `flags`
        if type(type_or_key) is str and type_or_key != 'auto':
            key_flags, type_or_key = Flags.from_typekey(type_or_key)
            flags |= key_flags

        # Handle `None` `val_`
        if val_ is None and flags & Flags.NULL:
            return self.null_string

        # Get `val_` type if `'auto'` passed to `type_or_key`
        if type_or_key == 'auto':
            type_or_key = type(val_)

        # Extract typekey from type if it supplied by `type_or_key`
        if isinstance(type_or_key, type):
            type_or_key = self.get_type_key(type_or_key)

        return self._resolve_dump_quotes(self._dump_by_key(val_, type_or_key), flags)

    def get_str_key(self, str_: str, flags: Flags = 0) -> str | None:

        flags: Flags = self._resolve_flags(flags)  # Handle input flags

        # Handle `null`-string
        if str_ in self._null_alias and flags & Flags.NULL:
            return None

        return self._get_str_key(self._resolve_load_quotes(str_, flags), flags)

    def get_str_type(self, str_: str, flags: Flags = 0) -> type:
        return self.get_key_type(self.get_str_key(str_, flags))

    def get_key_type(self, key_: str) -> type:
        return NoneType if key_ is None else self._get_key_type(key_)

    def get_type_key(self, type_: type) -> str:
        return None if type_ is NoneType or type_ is None else self._get_type_key(type_)

    # ------ Abstract methods

    @abstractmethod
    def _load_by_key(self, str_: str, key_: str, flags: Flags = 0) -> Any:
        """
        Internal method provides only loading from string by typekey.

        :param str_: normalized string value handled using flags
        :param key_: normalized typekey without flags mixes
        :param flags: flag, compiled by original `flags` & flags extracted from typekey

        :raise KeyError: if typekey not found
        :raise ValueError: if `val_` typekey not found or not supports load
        """

    @abstractmethod
    def _dump_by_key(self, val_: Any, key_: str, flags: Flags = 0) -> str:
        """
        Internal method provides only dump to string by typekey.

        :param val_: not-`None` input value
        :param key_: normalized typekey without flags mixes
        :param flags: flag, compiled by original `flags` & flags extracted from typekey

        :raise KeyError: if typekey not found
        :raise ValueError: if `val_` typekey not found or not supports dump
        """

    @abstractmethod
    def _get_type_key(self, type_: type) -> str:
        """
        Internal method, provides taking typekey from type.

        Input filtered from `None`/`NoneType` values.

        :raise TypeError: – if type is not supported
        """

    @abstractmethod
    def _get_key_type(self, key_: str) -> type:
        """
        Internal method, provides taking type from typekey.

        Input filtered from `None` typekeys.

        :raise KeyError: – if typekey not found
        """

    @abstractmethod
    def _get_str_key(self, str_: str, flags: Flags = 0):
        """
        Internal method provides only string value type recognition.

        :param str_: normalized string value handled using flags
        :param flags: flags passed to origin method

        :raise ValueError: if `str_` typekey was not recognized
        """

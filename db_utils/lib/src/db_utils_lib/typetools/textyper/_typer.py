from collections.abc import Iterable, Sequence, Mapping
from itertools import chain
from typing import Any
from copy import copy as do_copy

from .. import textypes, TypesMap
from . import TexTypeABC


class TexTyper(textypes.HandlerBase):
    """
    Fully configurable `textypes.Handler` with simple definition.

      Uses `TexTypeABC` instances to provide textypes definition and handling.
    """

    # ------ Protected fields

    _key_type: Mapping[str, TexTypeABC]     # Mapping of typekeys onto corresponding `TexTypeABC` instances
    _type_key: Mapping[type, str]           # Mapping types onto corresponding typekeys

    @property
    def types(self) -> Iterable[TexTypeABC]:
        """Iterable of defined textypes."""
        return self._key_type.values()

    # ------ Instantiation methods

    def __init__(self,
                 key_type: Mapping[str, TexTypeABC],
                 type_key: Mapping[type, str],
                 null_alias: Sequence[str] = None,
                 *, copy: bool = True):
        """
        Initializes new instance of `TexTyper` class.

          **WARNING**: This method depends on implementation details. It is strongly recommended not to use it directly.
          To instantiate `TexTyper` object use `new()` method instead.

        :param key_type: mapping of typekeys onto corresponding `TexTypeABC` instances
        :param type_key: mapping types onto corresponding typekeys
        :param null_alias: sequence of `null` value string alias - first value is default
                           (`('null',)` - by default)
        :param copy: whether to copy inputs
        """

        super().__init__(null_alias=(do_copy(null_alias) if copy else null_alias))

        self._key_type = do_copy(key_type) if copy else key_type
        self._type_key = do_copy(type_key) if copy else type_key

    @classmethod
    def new(cls,
            *types: TexTypeABC,
            null_alias: Sequence[str] = None,
            type_match_order: Iterable[str] = None,
            strict_type_match: bool = True) -> 'TexTyper':
        """
        Initializes new instance of `TexTyper` class.

        :param types: `TexTypeABC` instances to be included in typer -
                      passed order will be the same in string value textype match
        :param null_alias: sequence of `null` value string alias - first value is default
                           (`('null',)` - by default)
        :param type_match_order: iterable of typekeys, shows order of type match checks
                                 (unusable for strict-only type match)
        :param strict_type_match: whether to use strict-only type match (derived types match will fail)
                                  (`False` by default)
        """

        key_type = {txtp_.key: txtp_ for txtp_ in types}

        if type_match_order is not None:
            type_key = {key_type[key_].type: key_ for key_ in type_match_order}
        else:
            type_key = {txtp_.type: txtp_.key for txtp_ in types}

        if not strict_type_match:
            type_key = TypesMap(type_key, copy=False)

        return cls(key_type=key_type, type_key=type_key, null_alias=null_alias, copy=False)

    def __copy__(self):
        return self.__class__(key_type=self._key_type,
                              type_key=self._type_key,
                              null_alias=self._null_alias,
                              copy=False)

    def new_derived(self,
                    *types: TexTypeABC,
                    replace_types: bool = False,
                    reorder_types: Iterable[str] = None,
                    null_alias: Sequence[str] = None,
                    add_null_alias: Iterable[str] = None,
                    type_match_order: Iterable[str] = None,
                    strict_type_match: bool = True) -> 'TexTyper':
        """
        Initializes new instance of `TexTyper` class based on the current instance and inherits some of its data.

        :param types: `TexTypeABC` instances to be included in typer
        :param replace_types: whether to replace existed textypes with passed
        :param reorder_types: iterable of type keys, shoows order of types (will be the same in string value
                              textype match) - if not provided old/new/old+new types order will be used
        :param null_alias: sequence of `null` value string alias to replace existing
                           (not compatible with `add_null_alias` - it will be used instead if provided)
        :param add_null_alias: sequence of `null` value string alias to add to existing
        :param type_match_order: iterable of typekeys, shows order of type match checks
                                 (unusable for strict-only type match)
        :param strict_type_match: whether to use strict-only type match (derived types match will fail)
                                  (`False` by default)
        """

        # Form new `key_type` mapping
        if replace_types:
            key_type = {txtp_.key: txtp_ for txtp_ in types}
        else:
            key_type = dict(self._key_type)
            key_type.update((txtp_.key, txtp_) for txtp_ in types)

        # Reorder `key_type` if needed
        if reorder_types is not None:
            key_type = {key_: key_type[key_] for key_ in reorder_types}

        # Form new `null_alias` sequence
        if add_null_alias is not None:
            null_alias = list(chain(self.null_alias, add_null_alias))
        elif null_alias is None:
            null_alias = list(self.null_alias)

        # Form new `type_key` mapping
        if type_match_order is not None:
            type_key = {key_type[key_].type: key_ for key_ in type_match_order}
        else:
            type_key = {txtp_.type: txtp_.key for txtp_ in types}

        # Wrap `type_key` into `TypesMap` if needed
        if not strict_type_match:
            type_key = TypesMap(type_key, copy=False)

        # Construct & return new `TexTyper` instance
        return self.__class__(key_type=key_type, type_key=type_key, null_alias=null_alias, copy=False)

    # ------ Functionality methods

    def _get_key_type(self, key_: str) -> type:

        try:
            return self._key_type[key_].type

        except KeyError as e:
            raise KeyError(f"{key_} typekey not found.") from e

    def _get_type_key(self, type_: type) -> str:

        try:
            return self._type_key[type_]

        except KeyError as e:
            raise TypeError(f"{type_} type not found.") from e

    def _get_str_key(self, str_: str, flags: textypes.Flags = 0) -> str:

        for txtp_ in self.types:
            if txtp_.match(str_):
                return txtp_.key

        raise ValueError("String value was not recognized.")

    def _load_by_key(self, str_: str, key_: str, flags: textypes.Flags = 0) -> Any:

        try:
            return self._key_type[key_].load(str_)
        except KeyError:
            raise KeyError(f"'{key_}' typekey not found.")

    def _dump_by_key(self, val_: Any, key_: str, flags: textypes.Flags = 0) -> str:

        try:
            return self._key_type[key_].dump(val_)
        except KeyError:
            raise KeyError(f"'{key_}' typekey not found.")

from typing import TypeVar
from copy import copy as do_copy

from collections.abc import Iterable, Iterator, Mapping, ItemsView, KeysView, ValuesView


TValue_ = TypeVar('TValue_')


class TypesMap(Mapping[type, TValue_]):
    """
    Special helper to provides `collections.abc.Mapping` interface for mapping by types.

      To get value by type, it sequentially checks all stored types by `issubclass()` function
      and returns first matching result.
    """

    # ------ Protected fields

    _mapping: Mapping[type, TValue_]

    # ------ Instantiation methods

    def __init__(self, mapping: Mapping[type, TValue_] | Iterable[Iterable[type, TValue_]], *, copy: bool = True):
        """
        Initializes new instance of `MultiMatch` class.

        :param mapping: matches mapping as `collections.abc.Mapping` instance or iterable,
                        that can be converted into `dict`
        :param copy: whether to copy `mapping` value (will be ignored if `mapping` is not `collections.abc.Mapping`)
        """

        self._mapping = (do_copy(mapping) if copy else mapping) if isinstance(mapping, Mapping) else dict(mapping)

    # ------ Functionality methods

    def __getitem__(self, type_: type) -> TValue_:

        # First check for the exact match and get value in the fastest way if possible
        if type_ in self._mapping:
            return self._mapping[type_]

        # Run iterative search
        try:
            for match_, val_ in self._mapping.items():
                if issubclass(type_, match_):
                    return val_

        except TypeError:
            pass

        # Raise `KeyError` if nothing found
        raise KeyError(f"{type_} type not found.")

    # ------ Internal mapping wrapping methods

    def __len__(self) -> int:
        return len(self._mapping)

    def __iter__(self) -> Iterator[type]:
        return iter(self._mapping)

    def items(self) -> ItemsView[type, TValue_]:
        return self._mapping.items()

    def values(self) -> ValuesView[TValue_]:
        return self._mapping.values()

    def keys(self) -> KeysView[type]:
        return self._mapping.keys()

    # ------ `__copy__()` method

    def __copy__(self):
        return self.__class__(self._mapping, copy=True)

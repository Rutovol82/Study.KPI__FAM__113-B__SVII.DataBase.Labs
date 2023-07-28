from typing import TypeVar, Any
from collections.abc import Callable, Iterable, Mapping

from . import ContentMapper


TKey_ = TypeVar('TKey_')
TValue_ = TypeVar('TValue_')


class DictMapper(ContentMapper):
    """
    Content mapper wrapper for mappings.

      Build `ContentMapper` interface around object, implements `collection.abc.Mapping` interface.

        **NOTE**: It is recommended to use `as_mapper()` function to create `DictMapper` instances
        instead of direct `DictMapper` instantiation.
    """

    # ------ Protected fields

    _mapping: Mapping[TKey_, TValue_]    # Keys transformation callable

    # ------ Instantiation methods

    def __init__(self, mapping: Mapping[TKey_, TValue_]):
        """
        Initializes new instance of `DictMapper` class.

        :param mapping: source mapping
        """

        self._mapping = mapping

    # ------ Functionality methods

    def get_match(self, key: TKey_) -> TValue_:

        try:
            return self._mapping[key]

        # Catch mapping's `KeyError` and reraise `ValueError` specified in `get_match()` docs.
        except KeyError as e:
            raise ValueError(e)

    def try_get_match(self, key: TKey_, default: TValue_ = None) -> TValue_:

        # Override `try_get_match()` in purpose to directly use mapping's `get()` method.
        return self._mapping.get(key, default)

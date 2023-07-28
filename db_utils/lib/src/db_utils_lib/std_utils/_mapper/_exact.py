from collections.abc import Iterable, Mapping, Sequence
from typing import TypeVar, Literal

from db_utils_lib.std_helpers import Singleton

from . import ContentMapper


_T = TypeVar('_T')


class ExactMapper(ContentMapper[_T, _T], Singleton):
    """One of the simplest content mappers, designed just to be a stub for mapping objects onto themselves."""

    def get_match(self, obj: _T) -> _T:
        return obj

    def try_get_match(self, obj: _T, _: _T = None) -> _T:
        # Override method to avoid unnecessary operations
        return obj

    def try_get_matches(self,
                        keys: Iterable[_T],
                        _: Literal['exact', 'default'] = None,
                        __: _T = None) -> Sequence[_T]:

        # Override method to avoid unnecessary operations
        return self.get_matches(keys)

    def try_get_mapping(self,
                        keys: Iterable[_T],
                        _: Literal['exact', 'exclude', 'default'] = None,
                        __: _T = None) -> Mapping[_T, _T]:

        # Override method to avoid unnecessary operations
        return self.get_mapping(keys)

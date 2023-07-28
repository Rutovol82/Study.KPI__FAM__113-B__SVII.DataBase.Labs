from collections.abc import Iterable, Sequence, Mapping
from typing import Any, Literal

from db_utils_lib.std_helpers import Singleton

from . import ContentMapper


class EmptyMapper(ContentMapper[Any, Any], Singleton):
    """One of the simplest content mappers, designed just to be a stub to never found matching values."""

    def get_match(self, _: Any) -> Any:
        raise ValueError("Current ContentMapper is an EmptyMapper, it does not generates any matches never.")

    def try_get_match(self, _: Any, default: Any = None) -> Any:
        # Override method to avoid unnecessary operations
        return default

    def get_mapping(self, _: Any) -> Mapping[Any, Any]:
        # Override method to avoid unnecessary operations
        return self.get_match(_)

    def get_matches(self, _: Any) -> Sequence[Any]:
        # Override method to avoid unnecessary operations
        return self.get_match(_)

    def try_get_matches(self,
                        keys: Iterable[Any],
                        missing: Literal['exact', 'default'] = None,
                        default: Any = None) -> Sequence[Any]:

        # Override method to avoid unnecessary operations

        if missing == 'exact':
            return list(keys)

        if missing == 'default':
            return [default for _ in keys]

        if missing == 'exclude':
            return list()

        raise TypeError(f"Unknown 'missing' option '{missing}'")

    def try_get_mapping(self,
                        keys: Iterable[Any],
                        missing: Literal['exact', 'exclude', 'default'] = None,
                        default: Any = None) -> Mapping[Any, Any]:

        # Override method to avoid unnecessary operations

        if missing == 'exact':
            return {key: key for key in keys}

        if missing == 'default':
            return {key: default for key in keys}

        if missing == 'exclude':
            return dict()

        raise TypeError(f"Unknown 'missing' option '{missing}'")

from typing import Generic, TypeVar, Literal
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Sequence, Mapping

TKey_ = TypeVar('TKey_')
TValue_ = TypeVar('TValue_')


class ContentMapper(Generic[TKey_, TValue_], metaclass=ABCMeta):
    """
    Basic abstract class for content mappers.

      Provides an interface, allows to properly map input objects onto target objects.
    """

    @abstractmethod
    def get_match(self, key: TKey_) -> TValue_:
        """
        Get matching object for `key`.

        :raise ValueError: if match not found
        """

    def try_get_match(self, key: TKey_, default: TValue_ = None) -> TValue_:
        """Get matching object for `key` or return default value if not found."""

        # Default implementation just trying to use `get_match()` method
        # and returns default value if `ValueError` caught.
        try:
            return self.get_match(key)

        except ValueError:
            return default

    def get_matches(self, keys: Iterable[TKey_]) -> Sequence[TValue_]:
        """
        Get matching strings sequence for `keys`.

        :raise ValueError: if one of match
        """

        # Default implementation just calls `get_match()` method for each name
        return [self.get_match(key) for key in keys]

    def get_mapping(self, keys: Iterable[TKey_]) -> Mapping[TKey_, TValue_]:
        """
        Get matching strings dict for `keys`.

        :raise ValueError: if one of match
        """

        # Default implementation just calls `get_match()` method for each name
        return {key: self.get_match(key) for key in keys}

    def try_get_matches(self,
                        keys: Iterable[TKey_],
                        missing: Literal['exact', 'default'] = None,
                        default: TValue_ = None) -> Sequence[TValue_]:
        """
        Get matching strings sequence for `names`.

          Supports handling missing matches:

          * If `missing == 'exact'`, will match unmatched keys by themselves.
          * If `missing == 'default'`, will match unmatched keys by `default` value.

          `missing is None` - equivalent to '`default`'.

        :raise TypeError: if unknown `missing` literal was passed
        """

        # Default implementation depends on `try_get_match()` method

        if missing == 'default' or missing is None:
            return [self.try_get_match(key, default) for key in keys]

        if missing == 'exact':
            return [self.try_get_match(key, key) for key in keys]

        raise TypeError(f"Unknown 'missing' option '{missing}'")

    def try_get_mapping(self,
                        keys: Iterable[TKey_],
                        missing: Literal['exact', 'exclude', 'default'] = None,
                        default: TValue_ = None) -> Mapping[TKey_, TValue_]:
        """
        Get matching strings dict for `names`.

          Supports handling missing matches:

          * If `missing == 'exact'`, will map unmatched keys onto themselves.
          * If `missing == 'exclude'`, will exclude unmatched keys from resulting mapping.
          * If `missing == 'default'`, will map unmatched keys onto `default` value.

          `missing is None` - equivalent to '`default`'.

        :raise TypeError: if unknown `missing` literal was passed
        """

        # Default implementation depends on `get_match()` & `try_get_match()` methods

        if missing == 'default' or missing is None:
            return {key: self.try_get_match(key, default) for key in keys}

        if missing == 'exact':
            return {key: self.try_get_match(key, key) for key in keys}

        if missing == 'exclude':
            mapping = dict()
            for key in keys:
                try:
                    mapping[key] = self.get_match(key)
                except ValueError:
                    pass
            return mapping

        raise TypeError(f"Unknown 'missing' option '{missing}'")

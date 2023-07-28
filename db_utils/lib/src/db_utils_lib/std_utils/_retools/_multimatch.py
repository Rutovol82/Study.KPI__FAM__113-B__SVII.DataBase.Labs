from typing import TypeVar, Generic
from collections.abc import Iterable, Callable
from copy import copy as do_copy

import re


TValue_ = TypeVar('TValue_')


class MultiMatch(Generic[TValue_]):
    """
    A simple helper around the default `re.match()`/`re.fullmatch()`.

      Compiles and saves multiple match regex patterns and values corresponding to them during initialization
      and then provide an ability to perform sequential search among the patterns for matches with the input name
      and return the first matching pattern corresponding value.

        Originally designed to be a `ContentMapper`, so it is recommended to use it with `as_mapper()` wrapper.
    """

    # ------ Protected fields & public properties

    _mapping: list[tuple[re.Pattern, TValue_]]
    _matcher: Callable[[re.Pattern, str], re.Match]

    @property
    def mapping(self) -> Iterable[tuple[re.Pattern, TValue_]]:
        """
        Iterable of matching _patterns and corresponding values
        (represented by `(pattern: re.Pattern, value: TValue_)` tuples).
        """

        return iter(self._mapping)

    # ------ Instantiation methods

    def __init__(self, mapping: list[tuple[re.Pattern, str]], fullmatch: bool = True, *, copy: bool = True):
        """
        Initializes new instance of `MultiMatch` class.

        :param mapping: matches mapping as list of tuples: `tuple(pattern: re.Pattern, value: str)`
        :param fullmatch: whether to use `re.fullmatch()` instead of `re.match()` (`True` by default)
        :param copy: whether to copy `mapping` value
        """

        self._mapping = do_copy(mapping) if copy else mapping
        self._matcher = re.fullmatch if fullmatch else re.match

    @classmethod
    def from_iter(cls, mapping: Iterable[Iterable[str | re.Pattern, TValue_]], fullmatch: bool = True) -> 'MultiMatch':
        """
        Initializes new instance of `MultiMatch` class.

          Taking substitution rules as an Iterable of Iterables with the next structure:

            `Iterable[Iterable[pattern: str | re.Pattern, value: TValue_]]`

        :param mapping: matches mapping as iterable of iterables
        :param fullmatch: whether to use `re.fullmatch()` instead of `re.match()` (`True` by default)
        :return: initialized `MultiMatch` instance
        """

        # noinspection PyTypeChecker
        return cls([(re.compile(next(nested)), next(nested)) for nested in map(iter, mapping)], fullmatch, copy=False)

    # ------ Functionality methods

    def __call__(self, str_: str) -> TValue_:
        """
        Tries to find regex match in stored patterns and return corresponding value.

        :raise ValueError: if no matches was found
        """

        try:
            return next((value for pattern, value in self._mapping if self._matcher(pattern, str_) is not None))
        except StopIteration:
            raise ValueError(f'Unable to found match for {str_}.')

    def __getitem__(self, str_: str) -> TValue_:
        """
        Tries to find regex match in stored patterns and return corresponding value.

        :raise KeyError: if no matches was found
        """

        try:
            return next((value for pattern, value in self._mapping if self._matcher(pattern, str_) is not None))
        except StopIteration:
            raise KeyError(f'Unable to found match for {str_}.')

    def get(self, str_: str, default: TValue_):
        return next((value for pattern, value in self._mapping if self._matcher(pattern, str_) is not None), default)

    # ------ `__copy__()` method

    def __copy__(self):
        return self.__class__(self._mapping, copy=True)

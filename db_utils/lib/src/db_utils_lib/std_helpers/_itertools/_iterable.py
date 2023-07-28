from collections.abc import Iterable, Iterator
from typing import TypeVar


# Define public visible members
__all__ = ['iterable']


_T = TypeVar('_T')


# noinspection PyPep8Naming
class iterable(Iterator[_T], Iterable[_T]):
    """
    Simple wrapper for those iterators, that's don't have `__iter__()` method.

      Defines both `__iter__()` (returning wrapped iterator)
      and `__next__()` (returning `next(wrapped iterator)`) methods.
    """

    _iterator: Iterator[_T]     # Wrapped iterator

    def __init__(self, iterator_: Iterator[_T]):
        """
        Initializes new instance of `iterable` class.

        :param iterator_: iterator to be used
        """

        self._iterator = iterator_

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return next(self._iterator)

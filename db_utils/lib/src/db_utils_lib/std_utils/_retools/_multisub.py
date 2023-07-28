from collections.abc import Iterable
from copy import copy as do_copy

import re
from functools import reduce


class MultiSub:
    """
    A simple helper around the default `re.sub()`.

      Compiles and saves multiple substitution regex patterns (& replacements) during initialization
      and then provide an ability to apply them sequentially to the input string using the default `re.sub()` function.
    """

    # ------ Protected fields & public properties

    _subs: list[tuple[re.Pattern, str]]

    @property
    def subs(self) -> Iterable[tuple[re.Pattern, str]]:
        """Iterable of replacement rules (represented by `(pattern: re.Pattern, repl: str)` tuples)."""

        return iter(self._subs)

    # ------ Instantiation methods

    def __init__(self, subs: list[tuple[re.Pattern, str]], *, copy: bool = True):
        """
        Initializes new instance of `MultiSub` class.

        :param subs: substitution rules as list of tuples: `tuple(pattern: re.Pattern, repl: str)`
        :param copy: whether to copy `subs` value
        """

        self._subs = do_copy(subs) if copy else subs

    @classmethod
    def from_iter(cls, subs: Iterable[Iterable[str | re.Pattern, str]]) -> 'MultiSub':
        """
        Initializes new instance of `MultiSub` class.

          Taking substitution rules as an Iterable of Iterables with the next structure:

            `Iterable[Iterable[pattern: str | re.Pattern, repl: str]]`

        :param subs: substitution rules as iterable of iterables
        :return: initialized `ReSubMapper` instance
        """

        # noinspection PyTypeChecker
        return cls([(re.compile(next(nested)), next(nested)) for nested in map(iter, subs)], copy=False)

    # ------ `__call__()` method

    def __call__(self, str_: str):
        """Performs `str_` transformation by sequential applying stored regex substitutions."""

        a = reduce(lambda match, sub: re.sub(sub[0], sub[1], match), self._subs, str_)
        return a

    # ------ `__copy__()` method

    def __copy__(self):
        return self.__class__(self._subs, copy=True)

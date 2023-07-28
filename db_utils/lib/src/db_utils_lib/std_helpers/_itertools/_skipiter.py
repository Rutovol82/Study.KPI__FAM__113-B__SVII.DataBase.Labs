from abc import ABC, abstractmethod
from collections.abc import Iterator, Iterable
from itertools import islice
from typing import TypeVar

from . import iterable


# Define public visible members
__all__ = ['SkipIterator', 'SkipIterable', 'skip', 'fskip']


_T = TypeVar('_T')


class SkipIterator(Iterator[_T], ABC):
    """
    Interface, extends default `Iterator` definition with additional `__skip__()` method,
    allows skipping some count of next iterations in most efficient way.

      **What does it mean?**

        So, let's take a look at the next example:

          We have some file reader reads file line-by-line, parses each line and returns them
          one-by-one on each `__next__()` call.

            Everything looks good until we are faced with the task of skipping a few lines.
            If we just invoke default `__next__()` lines parsing will be invoked for each skipped line
            despite we don't neet its results.

              Using a default-like `SkipIterator` instead of built-in `Iterator` can be a good solution to this problem.
              With it, we can implement special logic for `__skip__()` method that will just move a reading
              process forward and will not invoke parsing, saving time and computing resources.

                ====

      **How it works?**

        Similarly to default iterator, to define a skip-iterator, you mainly need to
        implement default `__next__()` + additional `__skip__()` methods.

          `__skip__()` method must have the next signature: `__skip__(self, __n: int = 1) -> int`

            Here `__n` parameter is a count of iterations to be skipped, and the return value is a
            number of really skipped iterations (it may be less than `__n` but only because of iterator exhausting).

              In this way, it is also easy to interpret return as `bool`: `bool()` conversion will give
              a `True` always except the case when `0` returned - the case of iterator exhausting without skip.

                ====

      **How to use it?**

        Similarly to default iterators, invoked usually by built-in `next()` function,
        there are special `skip()` functions with signature:

          `Skip(__i: SkipIterator | Iterator, __n: int) -> int`

            This function, as you can see, is both suitable for skip iterators and for default iterators.

              It automatically checks does object have `__skip__()` method and invokes it if yes,
              otherwise it uses default `__next__()` together with most efficient Python
              generator constructions & `itertools` functions implemented in C and works on C speeds.

                ====
    """

    def __skip__(self, __n: int = 1) -> int:
        """
        Tries to skip next `__n` iterations in the most efficient way.

        :param __n: count of iterations to be skipped
        :return: count of really skipped iterations until iterator exhaust (from `0` to `__n`)
        """

        # Default implementation relies on using of default `__next__()`
        # together with most efficient Python generator constructions & `itertools` functions
        # implemented in C and works on C speeds
        return sum(1 for _ in islice(iterable(self), __n))


class SkipIterable(Iterable[_T], ABC):
    """
    Interface redefines default `Iterable` for a little by making `__iter__()` method to
    return a `SkipIterator` instead of default `Iterator`.

      This class designed more for declarative needs than for real profits.
      You are free not to use it never, keeping to use skip iterators.
    """

    @abstractmethod
    def __iter__(self) -> SkipIterator[_T]:
        pass


def skip(__i: SkipIterator | Iterator, __n: int = 1) -> int:
    """
    Tries to skip `__i` iterator's next `__n` iterations in the most efficient way.

    :param __i: iterator
    :param __n: count of iterations to be skipped

    :raise TypeError: if `__i` is not iterator

    :return: count of really skipped iterations until iterator exhaust (from `0` to `__n`)
    """

    # Check if `__i` has a `__skip__()` method and invoke it if yes.
    if hasattr(__i, '__skip__'):
        return __i.__skip__(__n)

    # Use default `__next__()` together with most efficient Python generator constructions & `itertools` functions
    # implemented in C and works on C speeds - similarly to default `__skip__()` implementation
    # from `SkipIterator` class.
    else:
        return sum(1 for _ in islice(iterable(__i), __n))


def fskip(__i: SkipIterator | Iterator, __n: int = 1) -> int:
    """
    Tries to skip **all** of `__i` iterator's next `__n` iterations in the most efficient way.

      Simple and specific addition to the `skip()` function.
      Instead of count of really skipped iters returns `True` if all `__n` skips was done, `False` otherwise.

    :param __i: iterator
    :param __n: count of iterations to be skipped

    :raise TypeError: if `__i` is not iterator

    :return: `True` if all of `__n` iters was skipped, `False` otherwise
    """

    # Just use the `skip()` function
    return skip(__i, __n) == __n

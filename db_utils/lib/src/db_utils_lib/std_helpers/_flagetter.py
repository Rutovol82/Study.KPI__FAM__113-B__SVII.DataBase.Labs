from enum import Flag
from collections.abc import Iterable

from functools import reduce


# Define public visible members
__all__ = ['FlagGetterMixin']


class FlagGetterMixin(Flag):
    """`enum.Flag` mixin provides additional methods for obtaining flag values from various inputs."""

    @classmethod
    def get(cls, *flags: int | str) -> 'FlagGetterMixin':
        """
        Extracts flag value from arguments set, where each argument can be:

        * flag literal
        * flag value
        * int value

        :raise KeyError: if one of flags not found
        :raise TypeError: if one of `args` arguments has an unsupported type
        :return: compiled flag
        """

        return cls.from_iter(flags)

    @classmethod
    def from_iter(cls, flags: Iterable[int | str | Flag]):
        """
        Extracts flag value from iterable, contains values, that can be converted into flag value. It can be:

        * flag literal
        * flag value
        * int value

        :raise KeyError: if one of flags not found
        :raise TypeError: if one of `args` arguments has an unsupported type
        :return: compiled flag
        """

        def predicate(flag_: cls, x_: str) -> cls:
            """
            Predicate function to be passed in `functools.reduce()`.
            Obtains flag from argument value (`x_`)  and compiles it with `flag_` flag.
            """

            if type(x_) is str:
                x_flag_ = cls.from_literal(x_)
            elif type(x_) is int:
                x_flag_ = cls[x_]
            elif isinstance(x_, cls):
                x_flag_ = x_
            else:
                raise TypeError(f"Unsupported argument type {type(x_)}.")

            return flag_ | x_flag_

        # noinspection PyTypeChecker
        return reduce(predicate, flags, 0)

    @classmethod
    def from_literal(cls, __s: str) -> 'FlagGetterMixin':
        """
        Extracts flag value from literal.

          Literal must conform next points:

          * different flags in string must be split by ',' (allowed to add also any count of spaces)
          * flag names must match real flag names except case (will be ignored)

        :raise KeyError: if one of flags not found
        :return: compiled flag
        """

        def predicate(flag_: cls, x_: str) -> cls:
            """
            Predicate function to be passed in `functools.reduce()`.
            Obtains flag from `x_` raw string with its name and compiles it with `flag_` flag.
            """

            return flag_ | cls[x_.strip().upper()]

        # noinspection PyTypeChecker
        return reduce(predicate, __s.split(','), 0)

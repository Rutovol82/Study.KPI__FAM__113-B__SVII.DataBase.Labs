from collections.abc import Iterable

import re


class DBVersion(tuple):
    """
    Database version
    """

    def __new__(cls, *args: str | int | Iterable[int]):

        if len(args) == 1:

            if type(args[0]) is str:
                return cls.parse(args[0])

            if isinstance(args[0], int):
                vers = (args[0],)

            else:
                vers = args[0]

                try:
                    iter(vers)

                except StopIteration:
                    raise ValueError("Unexpected argument. Version string or numbers (iterable) expected.")

        else:
            vers = args

        if any(not isinstance(ver, int) or ver < 0 for ver in vers):
            raise ValueError("Incorrect version format. Version numbers must be non-negative integers.")

        return tuple.__new__(cls, args)

    def __str__(self):

        return '.'.join(map(str, self))

    _VERSION_FORMAT_TCHECK_PATTERN = re.compile(r"(\d+)(\.(\d+))*")

    @classmethod
    def is_version(cls, __s) -> bool:
        """
        Checks, does the passed string format satisfies db-version pattern.
        """

        return bool(cls._VERSION_FORMAT_TCHECK_PATTERN.fullmatch(__s))

    @classmethod
    def parse(cls, __s) -> 'DBVersion':
        """

        """

        if not cls.is_version(__s):
            raise ValueError()

    def __lt__(self, other):

        if not isinstance(other, DBVersion):
            return NotImplemented

        for self_ver, other_ver in zip(self, other):

            if self_ver == other_ver:
                continue

            return self_ver < other_ver

        return len(self) < len(other)

    def __le__(self, other):

        if not isinstance(other, DBVersion):
            return NotImplemented

        for self_ver, other_ver in zip(self, other):

            if self_ver == other_ver:
                continue

            return self_ver < other_ver

        return len(self) <= len(other)

    def __gt__(self, other):

        if not isinstance(other, DBVersion):
            return NotImplemented

        for self_ver, other_ver in zip(self, other):

            if self_ver == other_ver:
                continue

            return self_ver > other_ver

        return len(self) > len(other)

    def __ge__(self, other):

        if not isinstance(other, DBVersion):
            return NotImplemented

        for self_ver, other_ver in zip(self, other):

            if self_ver == other_ver:
                continue

            return self_ver > other_ver

        return len(self) >= len(other)

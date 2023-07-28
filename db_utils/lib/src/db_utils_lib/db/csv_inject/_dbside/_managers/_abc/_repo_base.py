from abc import ABCMeta

from ... import RepositoryInfo

from . import RepositoryManagerABC


class RepositoryManagerBase(RepositoryManagerABC, metaclass=ABCMeta):
    """
    Base class for implementation `RepositoryManagers` derived from `RepositoryManagerABC`.

    Provides default implementation for some routine moments.
    """

    # ------ Protected fields

    _info: RepositoryInfo

    # ------ Public properties

    @property
    def info(self) -> RepositoryInfo:
        return self._info

    # ------ Instantiation methods

    def __init__(self, info: RepositoryInfo):
        """
        :param info: target repository info represented by `RepositoryInfo` instance
        """

        self._info = info

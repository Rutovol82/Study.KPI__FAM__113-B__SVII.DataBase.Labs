from abc import ABCMeta, abstractmethod

from . import RepoManager


class RepoBase(metaclass=ABCMeta):
    """
    Data repository abstraction.

      Defines interface, allows manipulating data in datastorage-independent way.
    """

    @abstractmethod
    def get_manager(self) -> RepoManager:
        """Returns new :class:`RepoManager` instance associated with the current repository."""

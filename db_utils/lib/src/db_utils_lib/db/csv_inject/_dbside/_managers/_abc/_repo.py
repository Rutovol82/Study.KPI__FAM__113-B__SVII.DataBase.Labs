from abc import ABCMeta, abstractmethod

from ... import RepositoryInfo

from . import RepositoryContentManagerABC


class RepositoryManagerABC(metaclass=ABCMeta):
    """High-level interface for maximally comfortable db-side injections data repository management."""

    # ------ Informational properties

    @property
    @abstractmethod
    def info(self) -> RepositoryInfo:
        """Returns db-side repository info as `RepositoryInfo` instance."""

    # ------ Repository infrastructure management methods

    @abstractmethod
    def init(self):
        """
        Initializes db-side repository infrastructure (injections info table) if not.
        """

    @abstractmethod
    def drop(self):
        """
        Drops db-side repository infrastructure (injections info table) if exists.

          ****

        **WARNING**: This method provides a destructive operation. Make sure you know what you do!
        """

    # ------ Repository data management global methods

    @abstractmethod
    def clear(self):
        """
        Clears all data from the repository, defined by `repo` `RepositoryInfo` instance.

          ****

        **WARNING**: This method provides a destructive operation. Make sure you know what you do!

          ****

        **NOTE**: There are `prune()` method, allows deleting only records about completed injections.
        """

    @abstractmethod
    def prune(self):
        """
        Clears all records about COMPLETED injections from the repository, defined by `repo` `RepositoryInfo` instance.
        """

    # ------ Functional properties

    @property
    @abstractmethod
    def content(self) -> RepositoryContentManagerABC:
        """Manage repository content."""

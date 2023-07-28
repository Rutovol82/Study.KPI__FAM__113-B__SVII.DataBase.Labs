import psycopg2.extensions

from . import RepositoryInfo
from . import RepositoryManagerOnConn, RepositoryManagerOnDumper

from ...wrapper import Dumper


# noinspection PyPep8Naming
class repo_managers:
    """
    `RepositoryManager`'s factory. Takes `RepositoryInfo` and helps to create default `RepositoryManager`'s over it.

      Exists more as some syntax sugar element ;)
      But (maybe) can be really useful in some cases.
    """

    # ------ Protected fields & public properties

    _info: RepositoryInfo

    @property
    def info(self) -> RepositoryInfo:
        """Repository info represented by `RepositoryInfo` instance."""
        return self._info

    # ------ Instantiation methods

    def __init__(self, info: RepositoryInfo):
        """
        Initializes new instance of `repository` class.

        :param info: repository info represented by `RepositoryInfo` instance
        """

        self._info = info

    # ------ Managers factory methods

    def over_dumper(self, dumper_: Dumper, /, *, init: bool = True) -> RepositoryManagerOnDumper:
        """
        Creates `RepositoryManager` for managing repository on database side over `wrapper.Dumper` instance.

        :param dumper_: `wrapper.Dumper` instance
        :param init: whether to automatically init repository on the database side if not exists yet (`True` by default)
        """

        # Create repository manager instance
        manager_ = RepositoryManagerOnDumper(dumper_, info=self._info)

        # Initialize repository on the database side if needed
        if init:
            manager_.init()

        return manager_

    def over_conn(self, conn_: psycopg2.extensions.connection, /, *, init: bool = True) -> RepositoryManagerOnConn:
        """
        Creates `RepositoryManager` for managing repository on database side over `psycopg2.connection` instance.

        :param conn_: `psycopg2.connection` instance
        :param init: whether to automatically init repository on the database side if not exists yet (`True` by default)
        """

        # Create repository manager instance
        manager_ = RepositoryManagerOnConn(conn_, info=self._info)

        # Initialize repository on the database side if needed
        if init:
            manager_.init()

        return manager_

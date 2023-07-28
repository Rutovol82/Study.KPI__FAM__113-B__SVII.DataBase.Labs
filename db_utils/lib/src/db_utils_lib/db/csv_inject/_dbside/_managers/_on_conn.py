from collections.abc import Iterator
from typing import Literal, Any

import psycopg2.extensions

from .. import _operations

from . import RepositoryManagerBase
from . import RepositoryContentManagerABC

from .. import RepositoryInfo, Status
from ... import Config


# Define public visible members
__all__ = ['RepositoryManagerOnConn']


class RepositoryManagerOnConn(RepositoryManagerBase):
    """
    DB-side injection data repository `RepositoryManager` on top of `psycopg2.connection`.

      Useful for working in 'lite' mode - without dumper or for providing actions in operational method.

        **NOTE**: Any changes made by this manager will not be committed automatically,
        unless you specified `autocommit` mode in connection settings (which is not recommended
        because of some operations are executed by multiple queries).
    """

    # ------ Protected fields

    _connection: psycopg2.extensions.connection     # `psycopg2.connection` instance represents database connection
    _content_manager: RepositoryContentManagerABC   # Initialized content manager instance

    # ------ Instantiation methods

    def __init__(self, __conn: psycopg2.extensions.connection, /, info: RepositoryInfo):
        """
        Initializes new instance of `RepositoryManagerOnConn` class.

          **NOTE**: It is recommended not to instantiate `RepositoryManager`s directly
          but use `repo_managers` class methods instead.

        :param __conn: `psycopg2.connection` instance represents connection with the database
                       where the repository is stored
        :param info: repository info represented by `RepositoryInfo` instance
        """

        super().__init__(info=info)
        self._connection = __conn
        self._content_manager = self.ContentManager(self)

    # ------ Interface implementation methods & properties

    def init(self):
        _operations.init(self._connection, repo=self.info)

    def drop(self):
        _operations.drop(self._connection, repo=self.info)

    def clear(self):
        _operations.clear(self._connection, repo=self.info)

    def prune(self):
        _operations.prune(self._connection, repo=self.info)

    @property
    def content(self) -> RepositoryContentManagerABC:
        return self._content_manager

    # ------ Content manager implementation

    class ContentManager(RepositoryContentManagerABC):
        """
        Repository content manager for the `RepositoryManagerOnConn`.

          **NOTE**: Any changes made by this manager will not be committed automatically,
          unless you specified `autocommit` mode in connection settings (which is not recommended
          because of some operations are executed by multiple queries).
        """

        # ------ Protected fields

        _base: 'RepositoryManagerOnConn'

        # ------ Instantiation methods

        def __init__(self, __base: 'RepositoryManagerOnConn', /):
            """
            Initializes new instance of `RepositoryManagerOnConn.ContentManager` class.

              **WARNING**: This is a service method by design.
              It is highly recommended to use base `RepositoryManager` instance `content` property instead.
            """

            self._base = __base

        # ------ Interface implementation methods (general)

        def status_count(self) -> int:
            return _operations.status_count(
                self._base._connection, repo=self._base.info
            )

        def status_items(self) -> Iterator[tuple[str, Status]]:
            return _operations.status_items(
                self._base._connection, repo=self._base.info
            )

        def status_keys(self) -> Iterator[str]:
            return _operations.status_keys(
                self._base._connection, repo=self._base.info
            )

        def status_objs(self) -> Iterator[Status]:
            return _operations.status_objs(
                self._base._connection, repo=self._base.info
            )

        # ------ Interface implementation methods (CRUD)

        def status_select(self, __id: str | Config, *,
                          on_not_exist: Literal['default', 'insert', 'except'] = 'default',
                          default: Any | Status = None) -> Status | None:

            return _operations.status_select(
                self._base._connection, repo=self._base.info, id_=__id, on_not_exist=on_not_exist, default=default
            )

        def status_delete(self, __id: str | Config, *,
                          on_not_exist: Literal['default', 'insert', 'except'] = 'default',
                          default: Any | Status = None) -> Status | None:

            return _operations.status_delete(
                self._base._connection, repo=self._base.info, id_=__id, on_not_exist=on_not_exist, default=default
            )

        def status_insert(self, __id: str | Config, status_: Status, *,
                          on_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:

            return _operations.status_insert(
                self._base._connection, repo=self._base.info, id_=__id, status_=status_, on_exist=on_exist
            )

        def status_update(self, __id: str | Config, status_: Status, *,
                          on_not_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:

            return _operations.status_update(
                self._base._connection, repo=self._base.info, id_=__id, status_=status_, on_not_exist=on_not_exist
            )

        # ------ Interface implementation methods (actions)

        def status_increment(self, __id: str | Config, *, must_exist: bool = True) -> Status | None:
            return _operations.status_increment(
                self._base._connection, repo=self._base.info, id_=__id, must_exist=must_exist
            )

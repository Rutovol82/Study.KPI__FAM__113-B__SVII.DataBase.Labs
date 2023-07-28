from collections.abc import Iterator
from typing import Literal, Any

from functools import partial

from db_utils_lib.db.wrapper import Dumper, commit_after

from .. import _operations

from . import RepositoryManagerBase
from . import RepositoryContentManagerABC

from ... import Config
from .. import RepositoryInfo, Status


# Define public visible members
__all__ = ['RepositoryManagerOnDumper']


class RepositoryManagerOnDumper(RepositoryManagerBase):
    """
    DB-side injection data repository `RepositoryManager` on top of `wrapper.Dumper`.

      Useful for execution independent operations using `wrapper.Dumper`.

        **NOTE**: All changes made by this manager will be committed immediately.
    """

    # ------ Protected fields

    _dumper: Dumper     # Dumper instance manages db connection
    _content_manager: RepositoryContentManagerABC   # Initialized content manager instance

    # ------ Instantiation methods

    def __init__(self, dumper_: Dumper, /, info: RepositoryInfo):
        """
        Initializes new instance of `RepositoryManagerOnDumper` class.

          **NOTE**: It is recommended not to instantiate `RepositoryManager`s directly
          but use `repo_managers` class methods instead.

        :param dumper_: `wrapper.Dumper` instance encapsulates database operations execution
        :param info: repository info represented by `RepositoryInfo` instance
        """

        super().__init__(info=info)
        self._dumper = dumper_
        self._content_manager = self.ContentManager(self)

    # ------ Interface implementation methods & properties

    def init(self):
        self._dumper.execute(
            commit_after(
                partial(_operations.init, repo=self.info)
            )
        )

    def drop(self):
        self._dumper.execute(
            commit_after(
                partial(_operations.drop, repo=self.info)
            )
        )

    def clear(self):
        self._dumper.execute(
            commit_after(
                partial(_operations.clear, repo=self.info)
            )
        )

    def prune(self):
        self._dumper.execute(
            commit_after(
                partial(_operations.prune, repo=self.info)
            )
        )

    @property
    def content(self) -> RepositoryContentManagerABC:
        return self._content_manager

    # ------ Content manager implementation

    class ContentManager(RepositoryContentManagerABC):
        """
        Repository content manager for the `RepositoryManagerOnDumper`.

          **NOTE**: All changes made by this manager will be committed immediately.
        """

        # ------ Protected fields

        _base: 'RepositoryManagerOnDumper'

        # ------ Instantiation methods

        def __init__(self, __base: 'RepositoryManagerOnDumper', /):
            """
            Initializes new instance of `RepositoryManagerOnDumper.ContentManager` class.

              **WARNING**: This is a service method by design.
              It is highly recommended to use base `RepositoryManager` instance `content` property instead.
            """

            self._base = __base

        # ------ Interface implementation methods (general)

        def status_count(self) -> int:
            return self._base._dumper.execute(
                commit_after(
                    partial(_operations.status_count,
                            repo=self._base.info)
                )
            )

        def status_items(self) -> Iterator[tuple[str, Status]]:
            return self._base._dumper.execute(
                commit_after(
                    lambda __conn: iter(list(_operations.status_items(__conn, repo=self._base.info)))
                )
            )

        def status_keys(self) -> Iterator[str]:
            return self._base._dumper.execute(
                commit_after(
                    lambda __conn: iter(list(_operations.status_keys(__conn, repo=self._base.info)))
                )
            )

        def status_objs(self) -> Iterator[str]:
            return self._base._dumper.execute(
                commit_after(
                    lambda __conn: iter(list(_operations.status_objs(__conn, repo=self._base.info)))
                )
            )

        # ------ Interface implementation methods (CRUD)

        def status_select(self, __id: str | Config, *,
                          on_not_exist: Literal['default', 'insert', 'except'] = 'except',
                          default: Any | Status = None) -> Status | None:

            return self._base._dumper.execute(
                commit_after(
                    partial(_operations.status_select,
                            repo=self._base.info, id_=__id,
                            on_not_exist=on_not_exist, default=default)
                )
            )

        def status_delete(self, __id: str | Config, *,
                          on_not_exist: Literal['default', 'insert', 'except'] = 'except',
                          default: Any | Status = None) -> Status | None:

            return self._base._dumper.execute(
                commit_after(
                    partial(_operations.status_delete,
                            repo=self._base.info, id_=__id,
                            on_not_exist=on_not_exist, default=default)
                )
            )

        def status_insert(self, __id: str | Config, status_: Status, *,
                          on_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
            return self._base._dumper.execute(
                commit_after(
                    partial(_operations.status_insert,
                            repo=self._base.info, id_=__id,
                            status_=status_, on_exist=on_exist)
                )
            )

        def status_update(self, __id: str | Config, status_: Status, *,
                          on_not_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
            return self._base._dumper.execute(
                commit_after(
                    partial(_operations.status_update,
                            repo=self._base.info, id_=__id,
                            status_=status_, on_not_exist=on_not_exist)
                )
            )

        # ------ Interface implementation methods (actions)

        def status_increment(self, __id: str | Config, *, must_exist: bool = True) -> Status | None:
            return self._base._dumper.execute(
                partial(_operations.status_increment,
                        repo=self._base.info, id=__id,
                        must_exist=must_exist)
            )

from data_lib.repo_abc import RepoBase, RepoManager

from . import SQLAlchemyRepoManagerObjs, SQLAlchemyRepoManagerView, SQLAlchemyRepoManagerStat


class SQLAlchemyRepoManager(RepoManager,
                            SQLAlchemyRepoManagerObjs,
                            SQLAlchemyRepoManagerView,
                            SQLAlchemyRepoManagerStat):
    """`SQLAlchemy` application data repository `RepoManager` manager."""

    # ------ Instantiation methods

    def __init__(self, __base: RepoBase):
        """
        Initializes new instance of `SQLAlchemyRepoManager`.

          **WARNING**: This is a service method by design.
          It is highly recommended to use base repository `SQLAlchemyRepoBase` instance `get_manager()` method instead.

        :param __base: base data repository :class:`SQLAlchemyRepoBase` object
        """

        # Call superclass `__init__()`
        super().__init__(__base)

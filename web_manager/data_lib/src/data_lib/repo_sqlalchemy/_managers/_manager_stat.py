from data_lib.repo_abc import RepoManagerStat

from . import SQLAlchemyRepoManagerBase


class SQLAlchemyRepoManagerStat(SQLAlchemyRepoManagerBase, RepoManagerStat):
    """`SQLAlchemy` data repository :class:`RepoManagerStat` manager."""


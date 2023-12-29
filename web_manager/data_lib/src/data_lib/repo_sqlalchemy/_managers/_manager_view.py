from data_lib.repo_abc import RepoManagerView, RepoViewInteractive

from . import SQLAlchemyRepoManagerBase


class SQLAlchemyRepoManagerView(SQLAlchemyRepoManagerBase, RepoManagerView):
    """`SQLAlchemy` data repository :class:`RepoManagerView` manager."""

    def entity_view(self, __cls: type) -> RepoViewInteractive:
        pass

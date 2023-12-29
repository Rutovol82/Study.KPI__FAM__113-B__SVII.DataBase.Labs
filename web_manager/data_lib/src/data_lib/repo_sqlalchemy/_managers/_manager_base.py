from abc import ABCMeta

from sqlalchemy.orm import Session

from data_lib.repo_abc import RepoBase, RepoManagerBase


class SQLAlchemyRepoManagerBase(RepoManagerBase, metaclass=ABCMeta):
    """Base class for the `SQLAlchemy` application data repository managers."""

    # ------ Protected fields

    _base: RepoBase             # Base repository `SQLAlchemyRepoBase` instance
    _session: Session | None    # `SQLAlchemy` Session` instance provides interation with orm and database

    # ------ Instantiation methods

    def __init__(self, __base: RepoBase):
        """
        Base initialization method for classes derived from `SQLAlchemyRepoManagerBase`.

        :param __base: base data repository :class:`SQLAlchemyRepoBase` object
        """

        self._base = __base
        self._session = None

    # ------ `prepare()`/`release()` methods

    # noinspection PyProtectedMember
    def prepare(self) -> RepoManagerBase:

        # Obtain `SQLAlchemy` `Session` instance from the base repository
        # noinspection PyUnresolvedReferences
        self._session = self._base._get_session()

        return self

    def release(self):

        # Close `SQLAlchemy` `Session` and remove reference to it
        self._session.close()
        self._session = None

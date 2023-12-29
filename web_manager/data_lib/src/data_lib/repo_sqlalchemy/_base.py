import sqlalchemy
from sqlalchemy import Engine, create_engine, URL
from sqlalchemy.orm import sessionmaker, registry, Session

from ._model import mapping_assembler

from data_lib.repo_abc import RepoBase, RepoManager

from . import SQLAlchemyRepoManager


class SQLAlchemyRepoBase(RepoBase):
    """
    Data repository (`RepoBase` implementation) based onto `SQLAlchemy` ORM
    and so allows managing data storage using the most of the common relational databases.
    """

    # ------ Protected fields

    _specific_engine: Engine            # Configured `SQLAlchemy` `Engine` instance
    _mapper_registry: registry          # Reference to `SQLAlchemy` `orm.registry` instance, used to map data model
    _session_factory: sessionmaker      # Configured `SQLAlchemy` `sessionmaker` sessions factory

    # ------ Instantiation methods

    def __init__(self, db_url: str | sqlalchemy.URL = None, /, **db_url_parts: str):
        """
        Initializes new instance of `SQLAlchemyRepoBase`.

        :param db_url: `SQLAlchemy` database connection URL as :class:`str` or :class:`sqlalchemy.URL` instance
                       (if not provided, will be assembled using `URL.create()` with `db_url_parts`)
        :param db_url_parts: arguments to be passed into `sqlalchemy.URL.create()` method
                             in case when `db_url` is not provided
        """

        # Perform classes mapping
        self._mapper_registry = mapping_assembler.assemble_mapping(registry())

        # Initialize `SQLAlchemy` `Engine` & `sessionmaker` instances
        self._specific_engine = create_engine(db_url if db_url is not None else URL.create(**db_url_parts))
        self._session_factory = sessionmaker(self._specific_engine)

    # ------ Package-internal interface methods

    def _get_session(self, **kwargs) -> Session:
        """
        Produces new `SQLAlchemy` `Session` instance to be used in associated manager.

        :param kwargs: additional arguments to be passed into `Session` constructor
        :return: new `SQLAlchemy` `Session` instance
        """

        return self._session_factory(**kwargs)

    # ------ Management accessing methods

    def get_manager(self) -> RepoManager:

        # Instantiate and return `SQLAlchemyRepoManager` object
        return SQLAlchemyRepoManager(self)

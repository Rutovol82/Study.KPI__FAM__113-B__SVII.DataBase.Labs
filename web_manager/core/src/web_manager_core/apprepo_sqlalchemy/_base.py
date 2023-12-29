from collections.abc import Mapping, Callable
from typing import Any

import flask
import data_lib
import data_lib.repo_sqlalchemy

from web_manager_core.apparepo_abc import AppRepoBase


class SQLAlchemyAppRepoBase(AppRepoBase):
    """
    Application data repository (`AppRepoBase` implementation)
    based onto underlying :class:`data_lib.repo_sqlalchemy.SQLAlchemyRepoBase` instance.

      ----

    Configuring

      `SQLAlchemyRepoBase` must be instantiated in a `Flask` extension manner and
      configured through the `Flask` configuration system as required by the base :class:`AppRepoBase` abstraction.

        The next configuration properties are accepted:

        * `SQLALCHEMY_DRIVERNAME` - database driver name for the `SQLAlchemy`
        * `SQLALCHEMY_USERNAME` - database user username
        * `SQLALCHEMY_PASSWORD` - database user password
        * `SQLALCHEMY_DATABASE` - target database name
        * `SQLALCHEMY_HOST` - databse connection host
        * `SQLALCHEMY_PORT` - database connection port

        The exact location of the described above properties in the `Flask` application
        configuration dictionary can be configured during instantiation.
    """

    # ------ Protected fields

    # Underlying `data_lib.repo_abc.RepoBase` instance
    _repo: data_lib.repo_abc.RepoBase

    # `Flask` application config handler callable
    _config_handler: Callable[[Mapping[str, Any]], Mapping[str, Any]]

    # ------ `__init__()` & `init_app()`/`destruct()` methods

    def __init__(self, app: flask.Flask = None, *,
                 config_handler: Callable[[Mapping[str, Any]], Mapping[str, Any]] = None,
                 **kwargs):
        """
        Initializes new instance of `SQLAlchemyRepoBase`.

        :param app: `Flask` application instance (optional - if passed `init_app()` will be called immediately)
        :param config_handler: `Flask` application config handler callable - takes origin config mapping
                               and returns that one, containing target properties (optional)
        """

        # Initialize local fields
        self._config_handler = config_handler or (lambda __cfg: __cfg)

        # Call superclass `__init__()`
        super().__init__(app, **kwargs)

    def init_app(self, app: flask.Flask):

        # Obtain configuration mapping
        cfg_ = self._config_handler(app.config)

        # Build an underlying `data_lib.repo_sqlalchemy.SQLAlchemyRepoBase` instance
        self._repo = data_lib.repo_sqlalchemy.SQLAlchemyRepoBase(
            drivername=cfg_['SQLALCHEMY_DRIVERNAME'],
            username=cfg_.get('SQLALCHEMY_USERNAME'),
            password=cfg_.get('SQLALCHEMY_PASSWORD'),
            database=cfg_.get('SQLALCHEMY_DATABASE'),
            host=cfg_.get('SQLALCHEMY_HOST'),
            port=cfg_.get('SQLALCHEMY_PORT')
        )

        # Call superclass `init_app()`
        super().init_app(app)

    # ------ `RepoBase` interface methods

    def get_manager(self) -> data_lib.repo_abc.RepoManager:

        # Pass call to the underlying `data_lib.repo_abc.RepoBase` instance
        return self._repo.get_manager()

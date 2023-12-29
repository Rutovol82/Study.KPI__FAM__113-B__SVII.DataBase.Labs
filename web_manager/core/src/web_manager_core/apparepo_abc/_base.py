from abc import ABCMeta

import flask
import data_lib


class AppRepoBase(data_lib.repo_abc.RepoBase, metaclass=ABCMeta):
    """
    Application data repository abstraction.

      An extension of the :class:`data_lib.repo_abs.RepoBase` abstraction,
      specially fitted for the `Flask` applications.

        Subclasses must use a `Flask` extension instantiation manner
        and configuring through the `Flask` configuration system.
    """

    # ------ Protected fields

    _g_manager_key: str     # Associated repository manager key in the flask.g context

    # ------ `__init__()` & `init_app() methods

    def __init__(self, app: flask.Flask = None, *,
                 g_manager_key: str = 'repman',
                 **__):
        """
        Default initialization method for classes derived from the `AppRepoBase` class.

        :param app: `Flask` application instance (optional - if passed `init_app()` will be called immediately)
        :param g_manager_key: associated repository manager key in the `flask.g` context
        """

        # Initialize local fields
        self._g_manager_key = g_manager_key

        # Call `init_app()` if Flask application instance provided
        if app is not None:
            self.init_app(app)

    def init_app(self, app: flask.Flask):
        """
        Initializes and prepares application repository to work in a `Flask` extension manner.

        Takes `Flask` application instance as an only positional argument.
        """

        @app.teardown_request
        def g_manager_release(_):
            """
            Releases request-local :class:`data_lib.repo_abc.RepoManager` instance
            associated with the current repository (if exists).
            """

            # Pop the repository manager from the g context (if exists)
            g_manager: data_lib.repo_abc.RepoManager = flask.g.pop(self._g_manager_key, default=None)

            # Check if the repository manager exists - release if yes
            if g_manager is not None:
                g_manager.release()

    # ------ Request-local properties

    @property
    def manager(self) -> data_lib.repo_abc.RepoManager:
        """
        Request-local :class:`data_lib.repo_abc.RepoManager` instance
        associated with the current repository.
        """

        # Check if the repository manager is already in the g context - insert new if not
        if self._g_manager_key not in flask.g:

            # Obtain and prepare new RepoManager instance
            g_manager = self.get_manager().prepare()

            # Insert RepoManager into g context
            setattr(flask.g, self._g_manager_key, g_manager)

        # Return repository manager from the g context
        return flask.g.get(self._g_manager_key)

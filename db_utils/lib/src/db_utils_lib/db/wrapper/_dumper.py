from collections.abc import Callable
from typing import Any, ClassVar, ContextManager

from functools import reduce

from db_utils_lib.std_utils import RetryOpts, RetryManager, Parameterizable, Params

import psycopg2
import psycopg2.extensions

from ..data import SessionOpts

from loguru import logger


# Define public visible members
__all__ = ['Dumper', 'db_dumper']


class Dumper(ContextManager):
    """
    Helper class helps to keep `psycopg2` connection to `PostgreSQL` DB online through the automatic reconnections.

      Includes functionality to establish connection with the `PostgreSQL` DB using `psycopg2` module
      and execute transactional methods/functions using this connection.

        **NOTE**: This is a very simple wrapper, so it fully depends on `psycopg2` API in all aspects.
    """

    # ------ Static defaults

    DEFAULT_RE_CONN_OPTS: ClassVar[RetryOpts] = RetryOpts(interval=1, attempts=None)
    """Default database connection retry options."""

    DEFAULT_RE_EXEC_OPTS: ClassVar[RetryOpts] = RetryOpts(interval=None, attempts=None)
    """Default operations execution retry options."""

    DEFAULT_SESSION_OPTS: ClassVar[SessionOpts] = SessionOpts()
    """Default `psycopg2` `connection` session options."""

    # ------ Protected fields

    _re_conn_opts: RetryOpts  # Database connection retry options
    _re_exec_opts: RetryOpts  # Operations execution retry options

    _conn_params: Parameterizable  # Parameters to be passed into `psycopg2.connect()`

    _connection: psycopg2.extensions.connection     # Actual `psycopg2` `connection` object
    _session_opts: SessionOpts      # `psycopg2` `connection` session options to be passed into `set_session()` method

    # ------ Properties getters/setters & getters/setters-alike methods

    @property
    def re_conn_opts(self) -> RetryOpts:
        """Database connection retry options to be applied in case of connection error occurrence."""
        return self._re_conn_opts

    @re_conn_opts.setter
    def re_conn_opts(self, value: RetryOpts):
        self._re_conn_opts = value

    @property
    def re_exec_opts(self) -> RetryOpts:
        """Operations execution retry options to be applied in case of connection error occurrence."""
        return self._re_exec_opts

    @re_exec_opts.setter
    def re_exec_opts(self, value: RetryOpts):
        self._re_exec_opts = value

    @property
    def connection(self) -> psycopg2.extensions.connection | None:
        """Actual `psycopg2` `connection` object."""
        return self._connection

    @property
    def session_opts(self):
        """`psycopg2` `connection` session options to be passed into `set_session()` method."""
        return self._session_opts

    @session_opts.setter
    def session_opts(self, value: SessionOpts):
        """`psycopg2` `connection` session options to be passed into `set_session()` method."""

        if self._connection is not None:
            value.apply(self._connection)

        self._session_opts = value

    def set_session_opts(self, *args, **kwargs):
        """Creates new instance of `SessionOpts` with passed args & kwargs and sets it to `session_opts` property."""

        self.session_opts = SessionOpts(*args, **kwargs)

    # ------ Instantiation methods

    def __init__(self,
                 conn_params: Parameterizable,
                 session_opts: SessionOpts = None,
                 re_conn_opts: RetryOpts = None, re_exec_opts: RetryOpts = None):
        """
        Initializes new instance of `Dumper` class.

        :param conn_params: parameters to be passed into `psycopg2.connect()` method, packed by `Parameterizable`
                            **NOTE**: It is recommended to use `db.data.ConnParams` instance for this argument.
        :param session_opts: `psycopg2` `connection` session options (`DEFAULT_SESSION_OPTS` by default)
        :param re_conn_opts: database connection retry parameters (`DEFAULT_RE_CONN_OPTS` by default)
        :param re_exec_opts: operations execution retry parameters (`DEFAULT_RE_EXEC_OPTS` by default)
        """

        self._conn_params = conn_params

        # Handle input `session_opts` and set `_session_opts` value
        self._session_opts = session_opts if session_opts is not None else self.DEFAULT_SESSION_OPTS

        # Handle input retry options and set to corresponding fields
        self._re_conn_opts = re_conn_opts if re_conn_opts is not None else self.DEFAULT_RE_CONN_OPTS
        self._re_exec_opts = re_exec_opts if re_exec_opts is not None else self.DEFAULT_RE_EXEC_OPTS

        # Configure and save logger
        self._logger = logger

    # ------ connect()/disconnect() & context manager support

    def connect(self):
        """
        Tries to establish connection with a database through the `psycopg2.connect()` method.

          ----

        On non-breaking failure will retrie a connection attempt according
        to the reconnection options (`reconn_opts` property).

          Non-breaking failure identified by occurrence of `psycopg2.InternalError`, `psycopg2.OperationalError`
          or `psycopg2.InterfaceError`.

            If reach reconnection attempts limit (only if configured in `re_conn_opts`)
            will reraise the last occurred error.

          ----

        :except psycopg2.InternalError, psycopg2.OperationalError, psycopg2.InterfaceError:
        on reach reconnection attempts limit (only if configured in `re_conn_opts`)
        :except psycopg2.Error:
        on any other exceptional situation

        :return: self
        """

        retrier_ = RetryManager(self._re_conn_opts)

        while True:
            try:

                logger.info("DB-DUMPER: trying to connect to database...")

                self._connection = psycopg2.connect(*self._conn_params.args, **self._conn_params.kwargs)
                self._session_opts.apply(self._connection)

                break

            except (psycopg2.InternalError, psycopg2.OperationalError, psycopg2.InterfaceError) as e:

                if retrier_.hasnext():
                    self._logger.info(f"DB-DUMPER: connection failed, retry in {retrier_.options.interval} s.")
                    retrier_.attempt()

                else:
                    self._logger.opt(exception=e).error(
                        f"DB-DUMPER: connection failed after {retrier_.counter} attempts.")

                    raise

            except psycopg2.Error as e:

                self._logger.opt(exception=e).error(
                    "DB-DUMPER: connection failed because of unexpected psycopg2 exception.")

                raise

        self._logger.success(f"DB-DUMPER: connection established on {retrier_.counter} attempt.")

        return self

    def disconnect(self):
        """Calls `connection.close()` method on actual `psycopg2.connection` object, stored in `connection` property."""

        self._connection.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # ------ Primary functional methods

    def execute(self, *ops: Callable[[psycopg2.extensions.connection], Any]) -> Any:
        """
        Tries to execute database operations, defined in `ops` callables.
        Execution order will be the same as passed.

          Take into account that wrapper will return output **ONLY** from the last operation callable.

          ----

        To be supported, operation callable must accept call-case
        with only one positional argument - `psycopg2.connection` object,
        that must be used inside `operation` to execute all database operations.

          ----

        On non-breaking failure will try to reconnect to database, according to the reconnection options
        (`reconn_opts` property), then retrie to execute operation.

          Non-breaking failure identified by occurrence of `psycopg2.InternalError`, `psycopg2.OperationalError`
          or `psycopg2.InterfaceError`.

            If operation fails again will repeat this procedure
            according to the re-execution options (`re_exec_opts` property).

              On reach reconnection attempts limit (only if configured in `re_exec_opts`)
              will reraise the last occurred exception.

          ----

        **NOTE**: If breaking failure occurs during reconnection -
        it will also break the execution process and produce exception

          ----

        :param ops: operations execution callables

        :except psycopg2.InternalError, psycopg2.OperationalError, psycopg2.InterfaceError:
        on reach reconnection / re-execution attempts limit (only if configured in `reconn_opts`/`reexec_opts`)
        :except psycopg2.Error:
        on any other exceptional situation

        :return: `operation` callable return
        """

        retrier_ = RetryManager(self._re_exec_opts)

        while True:
            try:
                self._logger.debug("DB-DUMPER: trying to execute operations sequence...")

                out_ = reduce(lambda _, op_: op_(self._connection), ops, None)

                self._logger.debug(f"DB-DUMPER: operations sequence executed on on {retrier_.counter} attempt.")

                return out_

            except (psycopg2.InternalError, psycopg2.OperationalError, psycopg2.InterfaceError) as e:

                if retrier_.hasnext():

                    logger.info(f"DB-DUMPER: operations sequence failed, "
                                f"reconnect & retry in {retrier_.options.interval} seconds.")

                    retrier_.attempt()
                    self.disconnect()
                    self.connect()

                else:
                    self._logger.opt(exception=e).error(
                        f"DB-DUMPER: operations sequence failed after {retrier_.counter} attempts.")
                    raise

            except psycopg2.Error as e:

                self._logger.opt(exception=e).error(
                    "DB-DUMPER: operations sequence failed  because of unexpected psycopg2 exception.")

                raise


def db_dumper(*args, re_conn_opts: RetryOpts = None, re_exec_opts: RetryOpts = None, **kwargs):
    """
    Initializes new instance of `Dumper` class.

      Unlike to `Dumper.__init__()` takes connection parameters as args & kwargs
      and packs them by `Params` automatically. Then initializes `Dumper` instance in a normal way.

    :param args: positional arguments to be passed into `psycopg2.connect()` method.
    :param kwargs: keyword arguments to be passed into `psycopg2.connect()` method.
    :param re_conn_opts: database connection retry parameters (`DEFAULT_RE_CONN_OPTS` by default).
    :param re_exec_opts: operations execution retry parameters (`DEFAULT_RE_EXEC_OPTS` by default).
    :return: initialized `Dumper` instance.
    """

    return Dumper(conn_params=Params(args=list(args), kwargs=kwargs),
                  re_conn_opts=re_conn_opts, re_exec_opts=re_exec_opts)

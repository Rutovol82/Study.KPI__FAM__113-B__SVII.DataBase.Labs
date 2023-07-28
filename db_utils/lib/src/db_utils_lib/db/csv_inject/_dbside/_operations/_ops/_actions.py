import psycopg2.sql as pgsql

import psycopg2.extras
import psycopg2.extensions

from .... import Config, get_id
from ... import Status

from ... import RepositoryInfo
from .. import _sql as sql


# noinspection DuplicatedCode
def status_increment(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo,
                     id_: str | Config,
                     *, must_exist: bool = True) -> Status | None:
    """
    Increments `injected` count of already injected blocks in record by id extracted from id string
    or injection `Config` instance in the repository, defined by `repo` `RepositoryInfo` instance.
    Returns updated `Status` instance.

      ----

    `must_exist` parameter can be used to define behavior on case when `Status`
    with given id not found in the repository.

    * If `must_exist is True` -`KeyError` will be thrown if requested instance not found.
    * If `must_exist is False` - `None` will be returned if requested instance not found.

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    :param id_: injection id string or `Config` instance

    :param must_exist: whether to raise exception if `Status` with given id not found (`True` by default)
    :raise KeyError: if `Status` with given id not found and `must_exist` is `True`

    :return: updated `Status` instance for given injection id or `None` if not found and `must_exist` is `False`
    """

    id_ = get_id(id_)  # Obtain injection id string

    with __conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROW_INCREMENT_INJECTED.format(table=pgsql.Identifier(repo.table_name)), {'id': id_})
        data_ = cursor_.fetchone()

    # Check for success
    if data_ is not None:
        # noinspection PyArgumentList
        return Status(**data_)

    # Handle fail
    if must_exist:
        raise KeyError(f"Status for injection with id='{id_}' not found.")

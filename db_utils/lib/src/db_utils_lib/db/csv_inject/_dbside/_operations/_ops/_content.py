from dataclasses import asdict
from typing import Literal, Any

import psycopg2.sql as pgsql

import psycopg2.extras
import psycopg2.extensions

from .... import Config, get_id
from ... import Status

from ... import RepositoryInfo
from .. import _sql as sql


# Define public visible members
__all__ = ['status_select', 'status_delete', 'status_insert', 'status_update']


# noinspection DuplicatedCode
def status_select(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo, id_: str | Config,
                  *, on_not_exist: Literal['default', 'insert', 'except'] = 'default',
                  default: Any | Status = None) -> Status | None:
    """
    Selects `Status` by id extracted from id string or injection `Config` instance
    from the repository, defined by `repo` `RepositoryInfo` instance.

      ----

    `on_not_exist` parameter can be used to define behavior on case when `Status`
    with given id not found in the repository. It can take next values:

    * '`default`' - if not exists do nothing & return `default` value
    * '`insert`' - if not exists insert `default` instance & return it
    * '`except`' - if not exists raise KeyError (default)

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    :param id_: injection id string or `Config` instance

    :param default: default value - may be returned (& inserted) if given id not found - depends on `on_not_exist` mode
    :param on_not_exist: literal defines what to do if `Status` with given id not exists
    :raise TypeError: if `default` is not `Status` instance, but `on_not_exist` set to '`insert`'
    :raise KeyError: if `Status` with given id not found and `on_not_exist` set to `except`

    :return: `Status` instance for given injection id or `default` if not found and `on_not_exist` set to '`default`'
    """

    # Handle default value type
    if on_not_exist == 'insert' and not type(default) is Status:
        raise TypeError("'on_not_exist' mode 'insert' implies that 'default' value must be a Status instance.")

    id_ = get_id(id_)  # Obtain injection id string

    with __conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROW_SELECT.format(table=pgsql.Identifier(repo.table_name)), {'id': id_})
        data_ = cursor_.fetchone()

    # Check for success
    if data_ is not None:
        # noinspection PyArgumentList
        return Status(**data_)

    # Handle fail
    if on_not_exist == 'default':
        return default
    elif on_not_exist == 'excpet':
        raise KeyError(f"Status for injection with id='{id_}' not found.")
    elif on_not_exist == 'insert':
        status_insert(__conn, repo=repo, id_=id_, status_=default, on_exist='except')
        return default
    else:
        raise ValueError(f"Unknown 'on_not_exist' literal value '{on_not_exist}'")


# noinspection DuplicatedCode
def status_delete(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo, id_: str | Config,
                  *, on_not_exist: Literal['default', 'except'] = 'default',
                  default: Any = None) -> Status | Any:
    """
    Deletes `Status` by id extracted from id string or injection `Config` instance
    from the repository, defined by `repo` `RepositoryInfo` instance.
    Returns deleted `Status` instance.

      ----

    `on_not_exist` parameter can be used to define behavior on case when `Status`
    with given id not found in the repository. It can take next values:

    * '`default`' - if not exists do nothing & return `default` value
    * '`except`' - if not exists raise KeyError (default)

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    :param id_: injection id string or `Config` instance

    :param default: default value - may be returned (& inserted) if given id not found - depends on `on_not_exist` mode
    :param on_not_exist: literal defines what to do if `Status` with given id not exists
    :raise KeyError: if `Status` with given id not found and `on_not_exist` set to `except`

    :return: deleted `Status` instance for given injection id or `default` if not found
             and `on_not_exist` set to '`default`'
    """

    id_ = get_id(id_)  # Obtain injection id string

    with __conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROW_DELETE.format(table=pgsql.Identifier(repo.table_name)), {'id': id_})
        data_ = cursor_.fetchone()

    # Check for success
    if data_ is not None:
        # noinspection PyArgumentList
        return Status(**data_)

    # Handle fail
    if on_not_exist == 'default':
        return default
    elif on_not_exist == 'excpet':
        raise KeyError(f"Status for injection with id='{id_}' not found.")
    else:
        raise ValueError(f"Unknown 'on_not_exist' literal value '{on_not_exist}'")


# noinspection DuplicatedCode
def status_insert(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo, id_: str | Config,
                  status_: Status, *, on_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
    """
    Places new `Status` by id extracted from id string or injection `Config` instance
    to the repository, defined by `repo` `RepositoryInfo` instance.

      ----

    `on_exist` parameter can be used to define behavior on case when `Status`
    with given id already exists in the repository. It can take next values:

    * '`ignore`' - on conflict do nothing & return `False`, otherwise return `True`
    * '`update`' - on conflict update existing instance, return `True` in both cases
    * '`except`' - on conflict raise KeyError, otherwise return `True` (default)

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    :param id_: injection id string or `Config` instance
    :param status_: injection id string or `Config` instance

    :param on_exist: literal defines what to do if `Status` with given id already exists
    :raise KeyError: if `Status` with given id not found and `on_exist` is `except`
    :raise ValueError: if unknown `on_exist` value passed

    :return: `True` on success, `False` otherwise (NOTE: 'success' depends on `on_exist` mode)
    """

    id_ = get_id(id_)  # Obtain injection id string

    with __conn.cursor() as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROW_INSERT.format(table=pgsql.Identifier(repo.table_name)),
                        {'id': id_, **asdict(status_)})
        flag_ = cursor_.fetchone()

    # Check for success
    if flag_ == (True,):
        return True

    # Handle fail
    if on_exist == 'ignore':
        return False
    elif on_exist == 'excpet':
        raise KeyError(f"Status for injection with id='{id_}' already exists.")
    elif on_exist == 'update':
        status_update(__conn, repo=repo, id_=id_, status_=status_, on_not_exist='except')
    else:
        raise ValueError(f"Unknown 'on_exist' literal value '{on_exist}'")


# noinspection DuplicatedCode
def status_update(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo, id_: str | Config,
                  status_: Status, *, on_not_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
    """
    Updates existing `Status` by id extracted from id string or injection `Config` instance
    in the repository, defined by `repo` `RepositoryInfo` instance.

      ----

    `on_not_exist` parameter can be used to define behavior on case when `Status`
    with given id not found in the repository. It can take next values:

    * '`ignore`' - if not exists do nothing & return `False`, otherwise return `True`
    * '`insert`' - if not exists insert new instance, return `True` in both cases
    * '`except`' - if not exists raise KeyError, otherwise return `True` (default)

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    :param id_: injection id string or `Config` instance
    :param status_: `Status` instance to update by

    :param on_not_exist: literal defines what to do if `Status` with given id not exists
    :raise KeyError: if `Status` with given id not found and `on_not_exist` is `except`
    :raise ValueError: if unknown `on_not_exist` value passed

    :return: `True` on success, `False` otherwise (NOTE: 'success' depends on `on_not_exist` mode)
    """

    id_ = get_id(id_)  # Obtain injection id string

    with __conn.cursor() as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROW_UPDATE.format(table=pgsql.Identifier(repo.table_name)),
                        {'id': id_, **asdict(status_)})
        flag_ = cursor_.fetchone()

    # Check for success
    if flag_ == (True,):
        return True

    # Handle fail
    if on_not_exist == 'ignore':
        return False
    elif on_not_exist == 'excpet':
        raise KeyError(f"Status for injection with id='{id_}' not found.")
    elif on_not_exist == 'insert':
        status_insert(__conn, repo=repo, id_=id_, status_=status_, on_exist='except')
    else:
        raise ValueError(f"Unknown 'on_exist' literal value '{on_not_exist}'")

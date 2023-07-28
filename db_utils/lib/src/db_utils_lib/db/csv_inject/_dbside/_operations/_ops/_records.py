from typing import Iterator

import psycopg2.sql as pgsql

import psycopg2.extras
import psycopg2.extensions

from ... import Status

from ... import RepositoryInfo
from .. import _sql as sql


# Define public visible members
__all__ = ['status_count', 'status_items', 'status_keys', 'status_objs']


# noinspection DuplicatedCode
def status_count(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> int:
    """
    Counts `Status` instances stored in the repository, defined by `repo` `RepositoryInfo` instance.

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance

    :return: stored `Status` records count
    """

    with __conn.cursor() as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROWS_COUNT.format(table=pgsql.Identifier(repo.table_name)))
        data_ = cursor_.fetchone()

    return data_[0]


# noinspection DuplicatedCode, PyTypeChecker
def status_items(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> Iterator[tuple[str, Status]]:
    """
    Returns iterator over tuples of injection id and `Status` instance for all records stored in the repository,
    defined by `repo` `RepositoryInfo` instance.

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance

    :return: iterator of tuples `(id: str, status: Status)`
    """

    with __conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROWS_ITEMS.format(table=pgsql.Identifier(repo.table_name)))

        # Fetch, cast and yield items one-by-one to stay in `with` context
        for data_ in cursor_:
            yield data_['id'], Status(injected=data_['injected'], completed=data_['completed'])


# noinspection DuplicatedCode, PyTypeChecker
def status_keys(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> Iterator[str]:
    """
    Returns iterator over injection id's for all records stored in the repository,
    defined by `repo` `RepositoryInfo` instance.

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance

    :return: iterator of injection id's strings
    """

    with __conn.cursor() as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROWS_KEYS.format(table=pgsql.Identifier(repo.table_name)))

        # Fetch and yield id's one-by-one to stay in `with` context
        for data_ in cursor_:
            yield data_[0]


# noinspection DuplicatedCode, PyTypeChecker
def status_objs(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> Iterator[Status]:
    """
    Returns iterator over injection `Status` instances for all records stored in the repository,
    defined by `repo` `RepositoryInfo` instance.

      ----

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance

    :return: iterator of injection `Status` instances
    """

    with __conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor_:
        # Execute query, fetch return
        cursor_.execute(sql.STATUS_ROWS_OBJS.format(table=pgsql.Identifier(repo.table_name)))

        # Fetch and yield id's one-by-one to stay in `with` context
        for data_ in cursor_:
            yield Status(**data_)

import psycopg2.sql as pgsql

import psycopg2.extensions

from ... import RepositoryInfo
from .. import _sql as sql


# Define public visible member
__all__ = ['init', 'drop', 'clear', 'prune']


# ------ Repository infrastructure management methods

# noinspection DuplicatedCode, PyTypeChecker
def init(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> None:
    """
    Initializes db-side repository infrastructure (injections info table) if not exists.

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    """

    with __conn.cursor() as cursor_:
        cursor_.execute(sql.INFO_TABLE_INIT.format(table=pgsql.Identifier(repo.table_name)))


# noinspection DuplicatedCode, PyTypeChecker
def drop(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> None:
    """
    Drops db-side repository infrastructure (injections info table) if exists.

      **WARNING**: This method provides a destructive operation. Make sure you know what you do!

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    """

    with __conn.cursor() as cursor_:
        cursor_.execute(sql.INFO_TABLE_DROP.format(table=pgsql.Identifier(repo.table_name)))


# ------ Repository data management global methods

# noinspection DuplicatedCode, PyTypeChecker
def clear(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> None:
    """
    Clears all data from the repository, defined by `repo` `RepositoryInfo` instance.

      **WARNING**: This method provides a destructive operation. Make sure you know what you do!

        ****

      **NOTE**: There are `prune()` method, allows deleting only records about completed injections.

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    """

    with __conn.cursor() as cursor_:
        cursor_.execute(sql.INFO_TABLE_CLEAR.format(table=pgsql.Identifier(repo.table_name)))


# noinspection DuplicatedCode, PyTypeChecker
def prune(__conn: psycopg2.extensions.connection, /, repo: RepositoryInfo) -> None:
    """
    Clears all records about COMPLETED injections from the repository, defined by `repo` `RepositoryInfo` instance.

    :param __conn: `psyvopg2.connection` instance, represents connection to target database
    :param repo: target repository `RepositoryInfo` instance
    """

    with __conn.cursor() as cursor_:
        cursor_.execute(sql.INFO_TABLE_CLEAR.format(table=pgsql.Identifier(repo.table_name)))

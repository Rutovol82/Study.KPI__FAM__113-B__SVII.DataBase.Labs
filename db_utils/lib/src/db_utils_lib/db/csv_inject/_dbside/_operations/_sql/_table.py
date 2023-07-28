from inspect import cleandoc

import psycopg2.sql as pgsql


# Define public visible members
__all__ = ['INFO_TABLE_INIT', 'INFO_TABLE_DROP', 'INFO_TABLE_CLEAR', 'INFO_TABLE_PRUNE']


INFO_TABLE_INIT: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        CREATE TABLE IF NOT EXISTS {table} 
        (
            id                  VARCHAR(100)    NOT NULL    PRIMARY KEY,
            injected            INTEGER         NOT NULL    DEFAULT 0,
            completed           BOOLEAN         NOT NULL    DEFAULT FALSE
        )
        """
    ))
"""
SQL query (`Postgres`), creates injections info table if not exists.

  -----

`format()` args:

* `table` - name of table, stores injections information

  ----
"""


INFO_TABLE_DROP: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        DROP TABLE IF EXISTS {table}
        """
    ))
"""
SQL query (`Postgres`), drops injections info table if exists.

  -----

`format()` args:

* `table` - name of table, stores injections information

  ----
"""


INFO_TABLE_CLEAR: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        TRUNCATE TABLE {table}
        """
    ))
"""
SQL query (`Postgres`), deletes all rows from injections info table.

  -----

`format()` args:

* `table` - name of table, stores injections information

  ----
"""


INFO_TABLE_PRUNE: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        DELETE FROM TABLE {table} WHERE completed
        """
    ))
"""
SQL query (`Postgres`), deletes from injections info table all rows where `completed = TRUE`.

  -----

`format()` args:

* `table` - name of table, stores injections information

  ----
"""

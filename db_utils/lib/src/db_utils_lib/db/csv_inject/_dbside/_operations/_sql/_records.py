from inspect import cleandoc

import psycopg2.sql as pgsql


# Define public visible members
__all__ = ['STATUS_ROWS_COUNT', 'STATUS_ROWS_ITEMS', 'STATUS_ROWS_KEYS', 'STATUS_ROWS_OBJS']


STATUS_ROWS_COUNT: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        SELECT count(*) FROM {table}
        """
    ))
"""
SQL query (`Postgres`), counts number of status records from the injections info table.

  ----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  Returns:

    Count of rows in info table == status records count.

  ----
"""


STATUS_ROWS_ITEMS: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        SELECT * FROM {table}
        """
    ))
"""
SQL query (`Postgres`), selects all columns across all rows from the injections info table.

  ----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  Returns:

    all columns values across all rows

  ----
"""


STATUS_ROWS_KEYS: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        SELECT id FROM {table}
        """
    ))
"""
SQL query (`Postgres`), selects `id` column across all rows from the injections info table.

  ----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  Returns:

    `id` column across all rows - all stored injection id's 

  ----
"""


STATUS_ROWS_OBJS: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        SELECT injected, completed FROM {table}
        """
    ))
"""
SQL query (`Postgres`), selects `injected` & `completed` columns across all rows from the injections info table.

  ----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  Returns:

    `injected` & `completed` columns across all rows - all stored injection statuses 

  ----
"""

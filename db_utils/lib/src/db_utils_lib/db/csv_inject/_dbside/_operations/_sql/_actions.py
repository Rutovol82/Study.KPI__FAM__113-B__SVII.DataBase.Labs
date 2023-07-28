from inspect import cleandoc

import psycopg2.sql as pgsql


# Define public visible members
__all__ = ['STATUS_ROW_INCREMENT_INJECTED']


STATUS_ROW_INCREMENT_INJECTED: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        UPDATE {table}
        SET injected = injected + 1
        WHERE id = %(id)s
        RETURNING injected, completed
        """
    ))
"""
SQL query (`Postgres`), increments `injected` value in status record in the injections info table by injection id.

  -----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  `execute()` args:

  * `id` - injection id

  ----

  Returns:

  * updated record `injected` & `completed` fields - on success
  * nothing - otherwise

  ----
"""

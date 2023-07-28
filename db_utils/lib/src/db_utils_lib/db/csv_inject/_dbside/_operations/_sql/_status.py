from inspect import cleandoc

import psycopg2.sql as pgsql


# Define public visible members
__all__ = ['STATUS_ROW_SELECT', 'STATUS_ROW_DELETE', 'STATUS_ROW_INSERT', 'STATUS_ROW_UPDATE']


STATUS_ROW_SELECT: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        SELECT injected, completed FROM {table} WHERE id = %(id)s
        """
    ))
"""
SQL query (`Postgres`), reads status record from the injections info table by injection id.

  ----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  `execute()` args:

  * `id` - injection id

  ----

  Returns:

  * requested record `injected` & `completed` fields - if exists
  * nothing - otherwise

  ----
"""


STATUS_ROW_DELETE: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        DELETE FROM TABLE {table} 
        WHERE id = %(id)s
        RETURNING injected, completed
        """
    ))
"""
SQL query (`Postgres`), deletes status record from the injections info table by injection id,
returns deleted row `injected` & `completed` columns.

  -----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  `execute()` args:

  * `id` - injection id

  ----

  Returns:
 
  * deleted record `injected` & `completed` fields - on success
  * nothing - if nothing deleted

  ----
"""


STATUS_ROW_INSERT: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        INSERT INTO {table} (id, injected, completed) 
        VALUES (%(id)s, %(injected)s, %(completed)s)
        ON CONFLICT DO NOTHING
        RETURNING TRUE
        """
    ))
"""
SQL query (`Postgres`), inserts new injection status record row in the info table, returns `TRUE` on success.

  -----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  `execute()` args:

  * `id` - injection id
  * `injected` - number of data blocks already injected in current injection
  * `completed` - whether the injection already completed

  ----

  Returns:

  * `TRUE` - on success
  * nothing - on `id` conflict

  ----
"""


STATUS_ROW_UPDATE: pgsql.SQL = \
    pgsql.SQL(cleandoc(
        """
        UPDATE {table}
        SET injected = %(injected)s,
            completed = %(completed)s
        WHERE id = %(id)s
        RETURNING TRUE
        """
    ))
"""
SQL query (`Postgres`), updates status record in the injections info table by injection id.

  -----

  `format()` args:

  * `table` - name of table, stores injections information

  ----

  `execute()` args:

  * `id` - injection id
  * `injected` - number of data blocks already injected in current injection
  * `completed` - whether the injection already completed

  ----

  Returns:

  * `TRUE` - on success
  * nothing - if nothing updated

  ----
"""

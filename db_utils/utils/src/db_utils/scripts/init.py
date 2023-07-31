import psycopg2.extensions
import psycopg2.sql as pgsql

from db_utils_lib.db.wrapper import Dumper, transactional

from importlib import resources

from .. import queries
from . import db_utils_command

from loguru import logger
from db_utils_lib.runtimer import runtimer


# Public members definition
__all__ = ['__command__', 'db_init']


# ------ Command script body

# Database initialization query (from resources)
_DB_INIT_QUERY = pgsql.SQL(resources.read_text(queries, 'init.sql'))


@transactional
def _init(__conn: psycopg2.extensions.connection):
    """Database initialization operation method."""

    with __conn.cursor() as cursor_:
        cursor_.execute(_DB_INIT_QUERY)


def db_init(dumper: Dumper):
    """
    Initialize 'zno-odata' database.

    :param dumper: `db.wrapper.Dumper` instance, manages db operations
    """

    logger.info("DB init: initialization started.")

    dumper.execute(_init)

    logger.success("DB init: initialization completed.")


# ------ Command script setup & entry point

@db_utils_command.entry_point(command='init', description="Initialize ZNO Open Data database.")
def __command__(dumper: Dumper, **__):
    """
    `init` command script entry point.

      Runs database injection procedure.

    :param dumper: `db.wrapper.Dumper` instance manages db operations
    """

    # Establish database connection and call initialization method
    with dumper:
        with runtimer(__name__):
            db_init(dumper)

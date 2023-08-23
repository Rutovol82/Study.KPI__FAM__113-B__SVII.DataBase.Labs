from collections.abc import Collection, Mapping
from typing import Any

import psycopg2.extras
import psycopg2.extensions
import psycopg2.sql as pgsql

from db_utils_lib.db.wrapper import Dumper
from db_utils_lib.db import csv_inject

from importlib import resources

from db_utils_lib.io.argparse import CompileFlag

from .. import queries
from . import db_utils_command

from .V1_1__init import db_init

# from loguru import logger
from db_utils_lib.runtimer import runtimer


# Public members definition
__all__ = ['__command__', 'db_injector']


# ------ Command script body

# noinspection PyPep8Naming
class db_injector:
    """'zno-odata' database injector to be used with `db.csv_inject.inject` api."""

    # ------ SQL queries class variables

    # Injection query pattern (from resources)
    _QUERY_PATTERN_INJECT = pgsql.SQL(resources.read_text(queries, 'V1_1__inject_row.query'))

    # ------ Protected fields

    _last_source_id: str = None             # Source id associated with last passed block
    _fmt_query: pgsql.Composable = None     # Query formatted for the currently passing source data blocks

    # ------ `__call__()` method

    def __call__(self, __conn: psycopg2.extensions.connection, block_: tuple[Collection[Mapping[str, Any]], str]):
        """
        Injects data block into 'zno-odata' database.

        :param __conn: `psycopg2.connection` instance, represents active database connection
        :param block_: data block tuple emitted by injection emitter
        """

        data_, source_id_ = block_  # Unpack block tuple

        # Check if source id changed - if yes - rebuild query and store new id
        if source_id_ != self._last_source_id:
            
            # Store the new source id
            self._last_source_id = source_id_

            # Extract property keys from the data
            properties_ = next(iter(data_)).keys()

            # Rebuild the injection query
            self._fmt_query = self._QUERY_PATTERN_INJECT.format(
                columns=pgsql.SQL(', ').join(pgsql.Identifier(prop_) for prop_ in properties_),
                values_placeholders=pgsql.SQL(', ').join(pgsql.Placeholder(prop_) for prop_ in properties_)
            )

        # Inject data to database row-by-row
        with __conn.cursor() as cursor_:
            psycopg2.extras.execute_batch(cursor_, self._fmt_query, data_)

    # ------ `inject()` class method

    @classmethod
    def inject(cls, config: csv_inject.Config, dumper: Dumper, repo: csv_inject.RepositoryInfo,
               cache: csv_inject.CacheInfo = None, mode: int | csv_inject.Mode = 0):
        """
        Run database injection procedure using a `db_injector` as `injector`.

          Just a wrapper for the `db.csv_inject.inject()` ;)

        :param config: current injection configuration as `Config` instance
        :param dumper: `wrapper.Dumper` instance manages database operations
        :param repo: db-side injections info repository specification
        :param cache: local injection data cache specification (optional)
        :param mode: injection `Mode` flags (optional)
        """

        return csv_inject.inject(config=config, dumper=dumper, injector=cls(), repo=repo, cache=cache, mode=mode)


# ------ Command script setup & entry point

@db_utils_command.entry_point(
    command='V1.1__inject',
    description="Injects data into ZNO Open Data database "
                "of V1.1 (#lab-1 #primary) schema. "
                "Injections configures mainly through the special "
                "injection config files in .yaml format",
    args=[
        ('cfg_path',
         dict(type=str,
              help='Path of injection config .yaml file.')),
        ('--cfg-encoding',
         dict(required=False, type=str, default='utf-8', dest='cfg_encoding',
              help='Injection config .yaml file encoding (UTF-8 by default).')),
        ('--inject-table',
         dict(required=False, type=str, default='injections', dest='inject_table',
              help='Name of table stores information about injections on database side.')),
        (('--mode', '-M'),
         dict(required=False, type=csv_inject.Mode, default=0, action=CompileFlag, dest='mode',
              help='Injection mode flags.')),
        (('--no-init', '-nI'),
         dict(required=False, dest='do_init', action='store_false',
              help='If passed, database initialization (in case if not initialized) will not be called.'))
    ]
)
def __command__(dumper: Dumper, cfg_path: str, cfg_encoding: str = None,
                inject_table: str = 'injections', do_init: bool = True,
                mode: int | csv_inject.Mode = 0, **__):
    """
    `V1.1__inject` command script entry point.

      Runs database injection procedure.

    :param dumper: `db.wrapper.Dumper` instance manages db operations
    :param cfg_path: path of injection config `.yaml` file
    :param cfg_encoding: injection config .yaml file encoding
    :param inject_table: name of table stores information about injections on the database side
    :param do_init: whether to initialize the database if not exists
    :param mode: injection mode flags
    """

    # Read config file
    from db_utils_lib.io import inject_config_loader
    config = inject_config_loader.loadconfig.from_file(cfg_path, encoding=cfg_encoding)

    # Construct `RepositoryInfo`
    repo = csv_inject.RepositoryInfo(table_name=inject_table)

    # Establish database connection
    with dumper:

        # Call database initialization if needed
        if do_init:
            with runtimer(__name__ + ' [init]'):
                db_init(dumper)

        # Run data injection
        with runtimer(__name__ + ' [inject]'):
            db_injector.inject(dumper=dumper, config=config, repo=repo, mode=mode | csv_inject.CACHE_DISABLE)

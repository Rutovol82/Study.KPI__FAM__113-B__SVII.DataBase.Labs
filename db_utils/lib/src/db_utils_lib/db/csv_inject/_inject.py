from collections.abc import Callable, Collection, Mapping, Iterator
from typing import Any

from db_utils_lib.std_helpers import skip, partialize

import psycopg2.extensions

from ..wrapper import Dumper, transactional

from . import Mode, REPO_NOT_INIT, CACHE_DISABLE
from . import InjectSplitter
from . import RepositoryInfo, repo_managers
from . import CacheInfo
from . import Config, Status

from loguru import logger
from db_utils_lib.runtimer import runtimer


# Define public visible members
__all__ = ['InjectOperator', 'inject']


class InjectOperator:
    """Class, implements automatic database injection procedure execution."""

    # ------ Operator setups (protected fields) & `_contextualize()` method

    _config: Config     # Current injection configuration as `Config` instance
    _dumper: Dumper     # `wrapper.Dumper` instance manages database operations

    # Callable to be called for each block
    _injector: Callable[[psycopg2.extensions.connection, tuple[Collection[Mapping[str, Any]], str]], Any]

    _db_repo: repo_managers     # Repository managers factory for the db-side repository

    _mode: int | Mode   # Injection `Mode` flags

    def _contextualize(self, __logger):
        """
        Calls `contextualize()` on `__logger` passing current injection context as args.

        :return: `__logger.contextualize()`  - logger contextualization contextmanager
        """

        return __logger.contextualize(
            injection_id=self._config.id,
            injection_mode=self._mode,
            cache_folder=None,
            db_side_repo=self._db_repo.info.table_name
        )

    # ------ Injection process data (protected fields)

    _status: Status     # Injection status, synchronized with db-side repository

    _emitter: Iterator[tuple[Collection[Mapping[str, Any]], str]]   # Emitter iterator for the current injection

    # ------ Instantiation & launch methods

    # noinspection PyUnusedLocal
    def __init__(
            self,
            config: Config,
            injector: Callable[[psycopg2.extensions.connection, tuple[Collection[Mapping[str, Any]], str]], Any],
            dumper: Dumper,
            repo: RepositoryInfo,
            cache: CacheInfo = None,
            mode: int | Mode = 0):
        """
        Initializes new instance of `InjectOperator` class.

          **NOTE**: It is recommended to use `inject()` function instead of `InjectOperator`
          manual instantiation and running.

        :param config: current injection configuration as `Config` instance
        :param injector: callable will be called for each block
        :param dumper: `wrapper.Dumper` instance manages database operations
        :param repo: db-side injections info repository specification
        :param cache: local injection data cache specification (optional)
        :param mode: injection `Mode` flags (optional)
        """

        self._config = config
        self._dumper = dumper

        self._injector = injector

        self._db_repo = repo_managers(repo)

        self._mode = mode

    def run(self):
        """
        Launches the injection process.

          **NOTE**: It is recommended to use `inject()` function instead of `InjectOperator`
          manual instantiation and running.
        """

        with self._contextualize(logger):

            logger.info(f"Injection '{self._config.id}': connecting to db repository...")

            # Create repo manager over dumper - for standalone operations
            repo_manager_ = self._db_repo.over_dumper(self._dumper, init=not self._mode & REPO_NOT_INIT)

            logger.debug(f"Injection '{self._config.id}': trying to obtain status from db repository...")

            # Obtain initial status from remote repository
            self._status = repo_manager_.content.status_select(self._config.id, on_not_exist='insert', default=Status())

            logger.info(f"Injection '{self._config.id}': obtained status from db repository.")

            # Check is injection already completed - finish if yes
            if self._status.completed:
                logger.info(f"Injection '{self._config.id}': injection already completed. Exit.")
                return

            logger.info(f"Injection '{self._config.id}': setting up emitter...")

            # Setup injection emitter and set to start block
            with runtimer(__name__ + f' [injection(id={self._config.id})/preparation]'):
                self._pull_blocks()
                skip(self._emitter, self._status.injected)

            logger.info(f"Injection '{self._config.id}': injection process starting.")

            # Run the injection process
            with runtimer(__name__ + f' [injection(id={self._config.id})/inject]'):
                self._push_blocks()

            logger.info(f"Injection '{self._config.id}': all blocks injected. Updating db repository info...")

            # Update status to `completed=True` & synchronize with repository
            self._status.completed = True
            repo_manager_.content.status_update(self._config.id, self._status)

            logger.success(f"Injection '{self._config.id}': completed.")

    # ------ Auxiliary methods

    def _push_blocks(self):
        """Sequentially injects blocks from emitter to database one-by-one."""

        for block_ in self._emitter:

            logger.info(
                f"Injection '{self._config.id}': block #{self._status.injected + 1}/$'{block_[1]}': injecting...")

            self._status = self._dumper.execute(self._inject_block(block_=block_))

            logger.success(
                f"Injection '{self._config.id}': block #{self._status.injected}/$'{block_[1]}': injected.")

    @partialize
    @transactional
    def _inject_block(self,
                      __conn: psycopg2.extensions.connection,
                      block_: tuple[Collection[Mapping[str, Any]], str]):
        """DB operation provides """

        # Run injector callable for the passed block
        self._injector(__conn, block_)
        return self._db_repo.over_conn(__conn).content.status_increment(self._config.id)

    def _pull_blocks(self):
        """Constructs an injection emitter object depending on injection mode."""

        if self._mode & CACHE_DISABLE:
            # Construct & return `InjectSplitter` instance
            self._emitter = iter(InjectSplitter(self._config))

        else:
            # Because of other options requires cache,
            # which is not implemented for now,
            # raise `NotImplementedError`
            raise NotImplementedError()


def inject(config: Config,
           injector: Callable[[psycopg2.extensions.connection, tuple[Collection[Mapping[str, Any]], str]], Any],
           dumper: Dumper,
           repo: RepositoryInfo,
           cache: CacheInfo = None,
           mode: int | Mode = 0):
    """
    Provides automatic database injection procedure execution.

    :param config: current injection configuration as `Config` instance
    :param injector: callable will be called for each block
    :param dumper: `wrapper.Dumper` instance manages database operations
    :param repo: db-side injections info repository specification
    :param cache: local injection data cache specification (optional)
    :param mode: injection `Mode` flags (optional)
    """

    operator_ = InjectOperator(config=config, injector=injector, dumper=dumper, repo=repo, cache=cache, mode=mode)

    with runtimer(__name__ + f' [injection(id={config.id})]'):
        operator_.run()

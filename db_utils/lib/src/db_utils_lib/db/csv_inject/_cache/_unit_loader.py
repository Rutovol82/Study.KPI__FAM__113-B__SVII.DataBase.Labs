from collections.abc import Mapping, Collection
from typing import Any

from db_utils_lib.std_helpers import SkipIterator, SkipIterable

from .. import Config

from ._meta import CacheUnitMeta
from ._intern import CacheUnitManager
from . import CacheInternalError


class CacheUnitLoader(SkipIterator[tuple[Collection[Mapping[str, Any]], str]],
                      SkipIterable[tuple[Collection[Mapping[str, Any]], str]]):
    """
    Class responsible for loading split and prepared injection data blocks from cache units.

    :raise CacheInternalError: on any internal error occurrence.
    """

    # ------ Protected fields

    _config: Config                 # Associated injection `Config` instance

    _unit_man: CacheUnitManager     # Current cache unit manager object
    _unit_meta: CacheUnitMeta       # Current unit metadata

    _block_num: int                 # Number of dumped blocks

    # ------ Instantiation methods

    def __init__(self, unit_: CacheUnitManager, meta_: CacheUnitMeta, config_: Config):
        """
        Initializes new instance of `CacheUnitLoader` class.

          **WARNING**: This is an internal method by design.
          `prepare()` method must be used for `CacheUnitLoader` instantiation.

        :param unit_: current cache unit manager
        :param meta_: preloaded cache unit metadata
        :param config_: unit target injection config as `Config` instance
        """

        self._config = config_

        self._unit_man = unit_
        self._unit_meta = meta_

        self._block_num = 0

    @classmethod
    def prepare(cls, unit_: CacheUnitManager, config_: Config) -> 'CacheUnitLoader':
        """
        Prepares new instance of `CacheUnitLoader` class.

          **WARNING**: This is a service method by design.
          It is highly recommended to use `get_loader()` method of parent `CacheManager` instead.

        :param unit_: current cache unit manager
        :param config_: unit target injection config as `Config` instance

        :raise CacheInternalError: on any internal error occurrence.

        :return: ready-to-work `CacheUnitLoader` instance
        """

        # Load unit metadata, create `CacheUnitLoader` instance and return
        return cls(unit_, unit_.load_meta(), config_)

    # ------ `__iter__()`, `__next__()` & `__skip__()` methods

    def __iter__(self) -> SkipIterator[tuple[Collection[Mapping[str, Any]], str]]:
        return self

    def __next__(self) -> tuple[Collection[Mapping[str, Any]], str]:

        # Check exhausting - raise `StopIteration` if yes
        if self._block_num >= self._unit_meta.n_blocks:
            raise StopIteration()

        # Increment block number
        self._block_num += 1

        try:
            # Load block metadata, obtain corresponding `Source` instance
            block_meta_ = self._unit_man.load_block_meta(self._block_num)
            source_ = self._config.sources[block_meta_.source_id]

            # Load data from block file
            with self._unit_man.block_csv_reader(self._block_num) as reader_:

                # Obtain properties names & typekeys from first two rows
                properties_ = next(reader_)
                typekeys_ = next(reader_)

                # Load block records to list
                data_ = [
                    {
                        prop_: source_.typing.types_handler.load(str_, key_)
                        for prop_, key_, str_
                        in zip(properties_, typekeys_, line_)
                    }
                    for line_ in reader_
                ]

        except (IOError, TypeError, ValueError) as e:
            raise CacheInternalError(e.args) from e

        # Return block records list & corresponding source id
        return data_, block_meta_.source_id

    def __skip__(self, __n: int = 1) -> int:

        # Get number of remaining blocks
        n_remains_ = self._unit_meta.n_blocks - self._block_num

        # Check if target in bounds
        if __n > n_remains_:

            # If not - set `_block_num` to border & return `n_remains_`
            self._block_num = self._unit_meta.n_blocks
            return n_remains_

        # If yes - move on `__n` blocks forward & return `__n`
        self._block_num += __n
        return __n

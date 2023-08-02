from collections.abc import Iterator, Mapping, Collection
from typing import ContextManager, Any

from .. import Config, Source

from ._meta import CacheUnitMeta, CacheBlockMeta
from ._intern import CacheUnitManager
from . import CacheInternalError


class CacheUnitDumper(ContextManager):
    """
    Class responsible for dumping injection data split on blocks into cache units.

      **NOTE**: It is recommended to use this class as context manager or
      through the `dump_whole()` method.
    """

    # ------ Protected fields

    _config: Config                 # Associated injection `Config` instance
    _unit_man: CacheUnitManager     # Current cache unit manager object

    _n_blocks: int                  # Number of dumped blocks

    _lst_source_id: str | None = None               # Source id associated with last dumped block
    _lst_source_info: Source | None = None          # `Source` instance associated with las dumped block
    _lst_properties: Collection[str] | None = None  # Last dumped block properties
    _lst_typekeys: Mapping[str, str] | None = None  # Last dumped block properties mapping on typekeys

    # ------ Instantiation methods

    def __init__(self, unit_: CacheUnitManager, config_: Config):
        """
        Initializes new instance of `CacheUnitDumper` class.

          **WARNING**: This is a service method by design.
          It is highly recommended to use `get_dumper()` method of parent `CacheManager` instead.

        :param unit_: current cache unit manager
        :param config_: unit target injection config as `Config` instance
        """

        self._config = config_
        self._unit_man = unit_

        self._n_blocks = 0

    # ------ Sequential writing methods

    def dump_block(self, block_: tuple[Collection[Mapping[str, Any]], str]):
        """
        Dumps data block to cache unit.

        :raise CacheInternalError: on any internal error occurrence.
        """

        data, source_id_ = block_

        # Check is current block source id the same as last - if no - update 'last' values
        if source_id_ != self._lst_source_id:

            # Update source info
            self._lst_source_id = source_id_
            self._lst_source_info = self._config.sources[source_id_]

            # Obtain properties from the first record keys
            self._lst_properties = next(iter(data)).keys()

            # Save map and typekeys
            self._lst_typekeys = self._lst_source_info.typing.types_map.try_get_mapping(
                self._lst_properties, default=self._lst_source_info.typing.extra_type
            )

        # Obtain current block number
        block_num_ = self._n_blocks + 1

        # Write data to block file
        with self._unit_man.block_csv_writer(block_num_) as writer_:

            try:
                # Write header and typekeys rows
                writer_.writerow(self._lst_properties)
                writer_.writerow(self._lst_typekeys.values())

                # Dump data
                writer_.writerows(
                    (
                        (self._lst_source_info.typing.types_handler.dump(rec_[prop_], self._lst_typekeys[prop_])
                        for prop_ in self._lst_properties)
                    )
                    for rec_ in data
                )

            except IOError as e:
                raise CacheInternalError(e.args) from e

        # Dump metadata for the current block
        self._unit_man.dump_block_meta(block_num_, CacheBlockMeta(source_id=source_id_))

        # Update dumped blocks counter
        self._n_blocks = block_num_

    def dump_blocks(self, blocks: Iterator[tuple[Collection[Mapping[str, Any]], str]]):
        """
        Dumps all data blocks from passed inject emitter to cache unit.

        :param blocks: object partially conforms to the inject emitter protocol - iterable returns tuples
                       of block records collection and associated source id (in the scope of current injection)
                       on each iteration
        :raise CacheInternalError: on any internal error occurrence.
        """

        # Just call `write_block()` for each block in data
        for block_ in blocks:
            self.dump_block(block_)

    # ------ `complete()` & `__exit__()` methods

    def complete(self):
        """
        Completes cache unit writing by dumping '.unit' file.

        :raise CacheInternalError: on any internal error occurrence.
        """

        # Dump unit metadata to file
        self._unit_man.dump_meta(CacheUnitMeta(n_blocks=self._n_blocks))

    def __exit__(self, exc_type, exc_value, traceback):

        # Complete dump only if no exceptions occurred
        if exc_type is None:
            self.complete()

    # ------ `dump_whole()` method

    def dump_whole(self, blocks: Iterator[tuple[Collection[Mapping[str, Any]], str]]):
        """
        Dumps all data blocks from passed inject emitter to cache unit and completes it.

        :param blocks: object partially conforms to the inject emitter protocol - iterable returns tuples
                       of block records collection and associated source id (in the scope of current injection)
                       on each iteration
        :raise CacheInternalError: on any internal error occurrence.
        """

        self.dump_blocks(blocks)
        self.complete()

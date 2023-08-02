import shutil
from contextlib import contextmanager

from os import PathLike
from pathlib import Path

import csv
import json

from dataclasses import asdict

from .. import _consts as consts
from .. import CacheInternalError
from .._meta import CacheUnitMeta, CacheBlockMeta


class CacheUnitManager:
    """
    Class encapsulates low-level access to the cache unit context.

      Provides methods for obtaining data blocks readers/writers,
      dumping & loading blocks and whole unit metadata.
    """

    # ------ Protected fields

    _folder: Path           # Cache unit root folder represented by `pathlib.Path` instance
    _unit_metafile: Path    # Pre-defined unit metadata file path as `pathlib.Path` instance

    # ------ Instantiation methods

    def __init__(self, folder: str | PathLike[str]):
        """
        Initializes new instance of `CacheUnitManager`

        :param folder:
        """

        self._folder = Path(folder)
        self._unit_metafile = self._folder.joinpath(consts.get_unit_meta_filename())

    # ------ Unit validation functionality

    def check_valid(self) -> bool:
        """Checks is the current cache unit exists and contains valid cache data."""

        # Check is directory exists
        if not self._folder.is_dir():
            return False

        # Check is 'unit.meta.json' metadata file exists
        if not self._folder.joinpath(consts.get_unit_meta_filename()).is_file():
            return False

        # Load metadata to provide further validation
        try:
            meta_ = self.load_meta()
        except CacheInternalError:
            return False

    # ------ Unit-level management

    def init(self):
        self._folder.mkdir()

    def drop(self):
        shutil.rmtree(self._folder)

    def dump_meta(self, data: CacheUnitMeta):
        """
        Dumps unit metadata (as `CacheUnitMeta` instance) to the current unit metadata file.

        :raise CacheInternalError: on any internal error occurrence.
        """

        try:
            with self._unit_metafile.open(mode='w', encoding=consts.get_unit_meta_encoding()) as f_:
                json.dump(asdict(data), f_)

        except (IOError, TypeError) as e:
            raise CacheInternalError(e.args) from e

    def load_meta(self) -> CacheUnitMeta:
        """
        Loads unit metadata (as `CacheUnitMeta` instance) from the current unit metadata file.

        :raise CacheInternalError: on any internal error occurrence.
        """

        try:
            with self._unit_metafile.open(mode='r', encoding=consts.get_unit_meta_encoding()) as f_:
                return CacheUnitMeta(**json.load(f_))

        except (IOError, json.JSONDecodeError, TypeError) as e:
            raise CacheInternalError(e.args) from e

    # ------ Block-level management

    def dump_block_meta(self, block_num: int, data: CacheBlockMeta):
        """
        Dumps cached data block metadata (as `CacheBlockMeta` instance)
        to the block metadata file by block number (`block_num`).

        :raise CacheInternalError: on any internal error occurrence.
        """

        try:
            with open(self._folder.joinpath(consts.get_block_meta_filename(block_num=block_num)),
                      mode='w', encoding=consts.get_block_meta_encoding()) as f_:

                json.dump(asdict(data), f_)

        except (IOError, TypeError) as e:
            raise CacheInternalError(e.args) from e


    def load_block_meta(self, block_num: int) -> CacheBlockMeta:
        """
        Loads cached data block metadata (as `CacheBlockMeta` instance)
        from the block metadata file by block number (`block_num`).

        :raise CacheInternalError: on any internal error occurrence.
        """

        try:
            with open(self._folder.joinpath(consts.get_block_meta_filename(block_num=block_num)),
                      mode='r', encoding=consts.get_block_meta_encoding()) as f_:

                return CacheBlockMeta(**json.load(f_))

        except (IOError, json.JSONDecodeError, TypeError) as e:
            raise CacheInternalError(e.args) from e

    @contextmanager
    def block_csv_writer(self, block_num: int, writer_factory=None, *args, **kwargs):
        """
        Contextmanager **ONLY** function. Takes care about block data file opening for writing,
        constructing `csv` writer (optionally using passed `writer_factory` and/or additional writer parameters).

          Returns `csv` writer constructed around opened `csv` file.

            **WARNING**: This MUST be used only with a `with` context -
            on the other hand, opened file will NOT be closed.

        :param block_num: data block number
        :param writer_factory: `csv` writer initializer - standard-alike `csv` writers signature expected
        :param args: additional positional arguments for the reader -
                     will be passed after `IO` object and before defaults
        :param kwargs: additional keyword arguents for the reader

        :raise CacheInternalError: on problems with file opening.

        :return: constructed `csv` reader around opened file
        """

        # Handle inputs & obtain constants
        writer_factory = csv.writer if writer_factory is None else writer_factory
        csv_opts = consts.get_block_data_csv_opts()

        # Try open file - raise `CacheInternalError` on fail
        try:
            f_ = open(self._folder.joinpath(consts.get_block_data_filename(block_num=block_num)),
                      mode='w', encoding=consts.get_block_data_encoding())

        except IOError as e:
            raise CacheInternalError(e.args) from e

        # Build & yield reader in protected mode
        try:
            yield writer_factory(f_, *args, *csv_opts.args, **kwargs, **csv_opts.kwargs)
        finally:
            # Close opened file
            f_.close()

    @contextmanager
    def block_csv_reader(self, block_num: int, reader_factory=None, *args, **kwargs):
        """
        Contextmanager **ONLY** function. Takes care about block data file opening for reading,
        constructing `csv` reader (optionally using passed `reader_factory` and/or additional reader parameters).

          Returns `csv` reader constructed around opened `csv` file.

            **WARNING**: This MUST be used only with a `with` context -
            on the other hand, opened file will NOT be closed.

        :param block_num: data block number
        :param reader_factory: `csv` reader initializer - standard-alike `csv` readers signature expected
        :param args: additional positional arguments for the reader -
                     will be passed after `IO` object and before defaults
        :param kwargs: additional keyword arguents for the reader

        :raise CacheInternalError: on problems with file opening.

        :return: constructed `csv` reader around opened file
        """

        # Handle inputs & obtain constants
        reader_factory = csv.reader if reader_factory is None else reader_factory
        csv_opts = consts.get_block_data_csv_opts()

        # Try open file - raise `CacheInternalError` on fail
        try:
            f_ = open(self._folder.joinpath(consts.get_block_data_filename(block_num=block_num)),
                      mode='r', encoding=consts.get_block_data_encoding())

        except IOError as e:
            raise CacheInternalError(e.args) from e

        # Build & yield reader in protected mode
        try:
            yield reader_factory(f_, *args, *csv_opts.args, **kwargs, **csv_opts.kwargs)
        finally:
            # Close opened file
            f_.close()

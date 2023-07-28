from collections.abc import Iterator, Collection, Mapping
from typing import Any, IO, ContextManager

from db_utils_lib.std_helpers import SkipIterator, SkipIterable, skip

from itertools import islice, chain

from .. import Config, Source
from . import SourceReader


class InjectSplitter(SkipIterator[tuple[Collection[Mapping[str, Any]], str]],
                     SkipIterable[tuple[Collection[Mapping[str, Any]], str]],
                     ContextManager):
    """
    Class, takes care about sequential reading all sources, mentioned in injection config,
    their normalization and splitting by atomic data blocks according to injection-global and source-specific options.

      According to injection emitter object contract implements `SkipIterable` interface,
      provides iterator, returns tuple of current data block records collection
      and associated source id on each iteration.

        ----

    **NOTE**: it is highly recommended to operate instances of `SourceSplitter`
    using the `with` operator - to grant that all opened source files will be properly closed.
    """

    # ------ Protected fields

    _config: Config     # `Config` instance stores current injection configuration data

    _queue: Iterator[tuple[str, Source]]    # Sources queue iterator

    _file: IO | None                                # Currently opened file object (`None` if no file opened)
    _reader: SkipIterator[dict[str, Any]] | None    # Current source file reader (`None` if no file opened)
    _source_id: str | None                          # Current source id (`None` if no file opened)
    _source_info: Source | None                     # Current source info (`None` if no file opened)

    # ------ __init__(), release() methods & context manager support

    def __init__(self, config: Config):
        """
        Initializes & prepares new instance of `InjectSplitter` class.

          **NOTE**: It is highly recommended to operate instances of `SourceSplitter`
          using the `with` operator - to grant that all opened source files will be properly closed.

        :param config: `Config` instance stores current injection config
        """

        # Store injection config & initialize sources queue
        self._config = config
        self._queue = iter(config.sources.items())

        # Set active file related fields to None
        self._file = None
        self._source_info = None
        self._reader = None

    def release(self):
        """Releases all currently active file resources used by `SourceSplitter`."""

        self._release_file()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    # ------ Service methods, responsible for work with files

    def _release_file(self):
        """Properly releases all resources associated with currently open file."""

        try:
            # Close currently opened file
            self._file.close()

        except (IOError, AttributeError):
            # Ignore possible exceptions
            pass

        finally:
            # Clear all links to related objects
            self._file = None
            self._reader = None
            self._source_id = None
            self._source_info = None

    def _prepare_file(self):
        """
        Properly opens and prepares the next file from queue.

        :raise StopIteration: if queue exhausted
        :raise IOError: if is raised by `open()`
        """

        # Get next source info
        # If queue exhausted, `StopIteration` will be raised here
        self._source_id, self._source_info = next(self._queue)

        # Open the next file
        # If something goes wrong - IOError may be raised here
        self._file = open(self._source_info.file.path, encoding=self._source_info.file.encoding)

        # Prepare reader for the current file - according to its behavior - must not throw any errors
        self._reader = SourceReader(self._file, self._source_info)

    # ------ `__iter__()`, `__next__()` & `__skip__()` methods

    def __iter__(self) -> SkipIterator[tuple[Collection[Mapping[str, Any]], str]]:
        return self

    def __next__(self) -> tuple[Collection[Mapping[str, Any]], str]:

        # Prepare active file if not prepared
        if self._file is None:
            self._prepare_file()

        # Create block iterator and try to get the first record
        block_ = islice(self._reader, self._config.options.atom_size)
        rec_0_ = next(block_, None)

        # If block has no first record - the current file seems to be exhausted.
        # Release it and call `__next__()` again
        if rec_0_ is None:
            self._release_file()
            return self.__next__()

        # Assemble back & collect to list, return block records collection & current source id
        return list(chain((rec_0_,), block_)), self._source_id

    def __skip__(self, __n: int = 1) -> int:

        # Try to prepare active file if not prepared, return 0 if queue exhausted
        if self._file is None:
            try:
                self._prepare_file()
            except StopIteration:
                return 0

        # Try to skip all `__n` blocks in the current file
        _sk_rows = skip(self._reader, __n * self._config.options.atom_size)

        # Calculate the number of really skipped blocks
        _sk_blocks = _sk_rows // self._config.options.atom_size
        _sk_blocks = _sk_blocks + 1 if (_sk_rows % self._config.options.atom_size > 0) else _sk_blocks

        # Check if the task done - if not - the current file seems to be exhausted.
        # Release it and call `__skip__()` again
        if _sk_blocks < __n:
            self._release_file()
            return _sk_blocks + self.__skip__(__n - _sk_blocks)

        return _sk_blocks

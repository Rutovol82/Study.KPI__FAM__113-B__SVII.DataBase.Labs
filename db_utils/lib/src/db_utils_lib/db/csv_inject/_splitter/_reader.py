from collections.abc import Sequence, Iterator, Iterable, Callable
from itertools import islice
from typing import Any

from db_utils_lib.std_helpers import iterable, SkipIterator, SkipIterable

import csv

from .. import Source


class SourceReader(SkipIterator[dict[str, Any]], SkipIterable[dict[str, Any]]):
    """
    Special reader for source `csv` data files (or other sources).

      Encapsulates work with columns & values formatting, types casting and including additional properties.

        Implements `Iterator`/`Iterable` protocols and returns `dict` with properties names
        as keys and values converted to Python types as values on each iteration.

          In that way, behavior mimics to `csv.DictReader`.
    """

    # ------ Protected fields

    _info: Source               # `Source` instance contains information about current source
    _data: Iterator[str]        # Raw data - iterator, returns raw string line per iteration
    _reader: Iterator[dict]     # Data reader - iterator, returns raw record elements list (`csv.reader`) per iteration

    _extras: dict[str, Any]     # Prepared additional properties mapping

    _typekeys: Sequence[str]                        # Built sequence of properties typekeys (properties order)
    _formatters: Sequence[Callable[[str], str]]     # Built sequence of properties value formatters (properties order)
    _properties: Sequence[str]                      # Built sequence of columns properties names (in columns order)

    # ------ Instantiation methods

    def __init__(self, data: Iterable[str], info: Source):
        """
        Initializes new instance of `SourceReader` class.

        :param data: `csv` data source - any `str` lines iterable, including a list of strings or text file
        :param info: `Source` instance, contains information about a current source
        """

        # Store `info`
        self._info = info

        # Obtain and store `data` iterator
        self._data = iter(data)

        # Skip first line if necessary
        if info.file.skip_head:
            next(self._data, None)

        # Create and store `csv.reader` instance for `data`
        self._reader = info.file.csv_opts.pass_to(csv.reader, iterable(self._data))

        # Obtain headers row if necessary
        headers = info.treatment.cols_names
        headers = headers if headers is not None else next(self._reader, None)

        # If file is not empty - built all necessary matching sequences
        if headers is not None:

            # Compile extra properties
            self._extras = {
                prop_: (
                    info.typing.types_handler.load(
                        self._info.treatment.vals_format_map.try_get_match(prop_, default=self._exact)(val_),
                        self._info.typing.types_map.try_get_match(prop_, default=self._info.typing.extra_type)
                    )
                    if type(val_) is str else val_
                )
                for prop_, val_ in self._info.properties.items()
            }

            # Build properties sequence
            self._properties = [
                (
                    info.treatment.cols_format_map.try_get_match(
                        col_, default=(col_ if info.treatment.cols_extra == 'keep' else None)
                    )
                    if col_ is not None and col_ not in info.treatment.cols_drop else None
                )
                for col_ in headers
            ]

            # Get temporary list of properties, filtered from `None`
            props_ = [prop_ for prop_ in self._properties if prop_ is not None]

            # Build formatters & typekeys sequences
            self._formatters = info.treatment.vals_format_map.try_get_matches(props_, default=self._exact)
            self._typekeys = info.typing.types_map.try_get_matches(props_, default=info.typing.extra_type)

    # ------ Functional methods

    def __iter__(self) -> SkipIterator[dict[str, Any]]:
        return self

    def __next__(self) -> dict[str, Any]:

        # Get next row sequence
        row_ = next(self._reader)   # If a source exhausted `StopIteration` will be raised here

        # Copy extras dictionary as output base
        rec_ = dict(self._extras)

        # Handle read values and add to record
        rec_.update(
            (prop_, self._info.typing.types_handler.load(format_(val_), typekey_))
            for (prop_, val_), format_, typekey_
            in zip(
                (pair for pair in zip(self._properties, row_) if pair[0] is not None),
                self._formatters, self._typekeys
            )
        )

        return rec_

    def __skip__(self, n_: int = 1) -> int:
        return sum(1 for _ in islice(self._data, n_))

    # ------ Service methods

    @staticmethod
    def _exact(s_):
        """
        Static stub to be used instead of lambda.
        One argument function. Always return this argument value.
        """

        return s_

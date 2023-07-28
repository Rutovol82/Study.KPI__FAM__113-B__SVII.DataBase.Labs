from dataclasses import dataclass, field

from os import PathLike
from db_utils_lib.std_utils import Parameterizable, frozen_params


@dataclass(frozen=True)
class SourceFile:
    """Dataclass for storing db injection source data file info."""

    path: str | PathLike[str]
    """Path to source `.csv` file."""

    encoding: str = 'utf-8'
    """Encoding of source `.csv` file."""

    csv_opts: Parameterizable = field(default_factory=frozen_params)
    """Options to be passed to `csv.reader`."""

    skip_head: bool = False
    """Whether to skip first line of source `.csv` file."""

from dataclasses import dataclass

from os import PathLike


@dataclass(frozen=True)
class CacheInfo:
    """Dataclass stores information about local injections data cache."""

    root_folder: str | PathLike[str]
    """Root cache directory path."""

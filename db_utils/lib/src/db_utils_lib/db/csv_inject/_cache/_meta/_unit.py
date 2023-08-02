from dataclasses import dataclass


@dataclass(frozen=True)
class CacheUnitMeta:
    """Dataclass represents cache unit metadata, stored in 'unit.meta.json' file."""

    n_blocks: int
    """Total count of data blocks in cached injection."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CacheBlockMeta:
    """Dataclass represents cached data block metadata, stored in a `*.block.meta.json` files."""

    source_id: str
    """Id of corresponding source in scope of the current injection."""

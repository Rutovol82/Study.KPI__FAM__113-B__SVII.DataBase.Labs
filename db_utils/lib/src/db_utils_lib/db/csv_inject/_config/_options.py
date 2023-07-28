from dataclasses import dataclass


@dataclass(frozen=True)
class Options:
    """Dataclass stores db data injection options."""

    atom_size: int = 1000
    """Amount of records to be inserted by one transaction."""

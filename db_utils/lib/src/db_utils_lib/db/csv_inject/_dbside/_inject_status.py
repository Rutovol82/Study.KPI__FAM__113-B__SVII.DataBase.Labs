from dataclasses import dataclass


@dataclass
class Status:
    """Dataclass represents db data injection status."""

    injected: int = 0
    """Number of data blocks already injected in current injection."""

    completed: bool = False
    """Whether the injection already completed."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryInfo:
    """Dataclass stores information about db-side injections info repository."""

    table_name: str
    """Name of table, stores injections information on the target database side."""

from dataclasses import dataclass


@dataclass
class Subject:
    """Dataclass represents **test subject**."""

    id: int
    """Subject id."""

    code: str
    """Subject code."""

    name: str = None
    """Subject name"""

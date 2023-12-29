from dataclasses import dataclass


# Define public visible members
__all__ = ['EduLang', 'EduProfile']


@dataclass
class EduLang:
    """Dataclass represents **language accepted to be used in education/testing**."""

    id: int
    """Language id."""

    name: str
    """Language name."""


@dataclass
class EduProfile:
    """Dataclass represents **educational profile**."""

    id: int
    """Profile id."""

    name: str
    """Profile name."""

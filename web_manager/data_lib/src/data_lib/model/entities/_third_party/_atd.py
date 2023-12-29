from dataclasses import dataclass


# Define public visible members
__all__ = ['Region', 'Area', 'Territory']


@dataclass
class Region:
    """Dataclass represents **ATD region**."""

    id: int
    """Region id."""

    name: str
    """Region name."""


@dataclass
class Area:
    """Dataclass represents **ATD region area**."""

    id: int
    """Area id."""

    name: str
    """Area name."""

    region_id: int
    """Parent region id."""


@dataclass
class Territory:
    """Dataclass represents **ATD area territory**."""

    id: int
    """Territory id."""

    name: str
    """Territory name."""

    area_id: int
    """Parent area id."""

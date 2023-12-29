from dataclasses import dataclass


# Define public visible members
__all__ = ['TestPoint']


@dataclass
class TestPoint:
    """Dataclass represents **testing point**."""

    id: int
    """Test point id."""

    name: str
    """Name of location/organization used as test point."""

    location_terr_id: int = None
    """Test point physical location territory id."""

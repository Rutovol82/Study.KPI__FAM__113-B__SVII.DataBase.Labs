from dataclasses import dataclass


# Define public visible members
__all__ = ['EduOrgType', 'EduSupervisor', 'EduOrganization']


@dataclass
class EduOrgType:
    """Dataclass represents **educational organizations type**."""

    id: int
    """Type id."""

    name: str
    """Type name."""


@dataclass
class EduSupervisor:
    """Dataclass represents **educational organization supervisor**."""

    id: int
    """Supervisor organization id."""

    name: str
    """Supervisor organization name."""


@dataclass
class EduOrganization:
    """Dataclass represents **educational organization**."""

    id: int
    """Educational organization id."""

    name: str
    """Educational organization name."""

    location_terr_id: int = None
    """Organization physical location territory id."""

    type_id: int = None
    """Educational organization type id."""

    supervisor_id: int = None
    """Supervisor organization id."""

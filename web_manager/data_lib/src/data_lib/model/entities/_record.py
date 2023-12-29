from dataclasses import dataclass


@dataclass
class Record:
    """Dataclass represents **OpenData record**."""

    id: str
    """Record OutID."""

    record_year: int
    """Record year."""

    examinee_id: int = None
    """Corresponding examinee data id."""

from dataclasses import dataclass, field
from typing import Any

from . import SourceFile, SourceTyping, SourceTreatment


@dataclass(frozen=True)
class Source:
    """Dataclass represents db data injection source info."""

    file: SourceFile
    """Source data file info."""

    typing: SourceTyping
    """Source data typing info."""

    treatment: SourceTreatment
    """Source data treatment options."""

    properties: dict[str, Any] = field(default_factory=dict)
    """Dictionary of additional properties, not included to source but exists and common for all of it's rows."""

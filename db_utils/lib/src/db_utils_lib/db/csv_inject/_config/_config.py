from dataclasses import dataclass, field
from collections.abc import Mapping

from . import Options, Source


@dataclass(frozen=True)
class Config:
    """Dataclass represents db data injection configuration."""

    id: str
    """Unique (for target database) name for current injection."""

    sources: Mapping[str, Source]
    """
    `Source` instances, defines data sources to be included in the current injection 
    with their id's - as keys (valid for the current injection only).
    
      **NOTE**: It is expected that `Mapping` contains `Source`'s will **SAVE KEYS ORDER**.
    """

    options: Options = field(default_factory=Options)
    """`Options` instance, contains current db injection options."""

from dataclasses import dataclass

from db_utils_lib.std_utils import ContentMapper
from db_utils_lib.typetools import textypes

from ... import DEFAULT_CSV_TYPER


@dataclass(frozen=True)
class SourceTyping:
    """Dataclass for storing db injection source data typing info."""

    types_map: ContentMapper[str, str]
    """`ContentMapper` to be used for producing mapping of records columns/properties onto corresponding typekeys."""

    extra_type: str = None
    """Typekey to be used for all properties not matched in `types_map`. Leave `None` if you don't need this option."""

    types_handler: textypes.HandlerABC = DEFAULT_CSV_TYPER
    """`textypes.HandlerABC` instance to be used for handling all type-dependent inject operations."""

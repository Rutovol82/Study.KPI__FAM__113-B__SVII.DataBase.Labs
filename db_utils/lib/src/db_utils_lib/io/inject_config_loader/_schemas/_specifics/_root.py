from marshmallow import Schema
from marshmallow.fields import Nested

from . import SpecificsFileSchema, SpecificsTypingSchema, SpecificsTreatmentSchema


# noinspection PyTypeChecker
class SourceSpecificsSchema(Schema):
    """Source specifics standalone file / local section `marshmallow` `Schema`."""

    file = Nested(SpecificsFileSchema, required=False)
    """Options dict to be passed to `csv.reader`."""

    typing = Nested(SpecificsTypingSchema, required=False)
    """Types definition & handling options section."""

    treatment = Nested(SpecificsTreatmentSchema, required=False)
    """Columns names and values processing options section.."""

import codecs

from marshmallow import Schema, validates, ValidationError
from marshmallow.fields import Str


class FileInfoSchema(Schema):
    """Base schema to validate basic file input credentials"""

    path = Str()
    """Path to standalone source specifics file."""

    encoding = Str(required=False)
    """Encoding of standalone source specifics file."""

    @validates('encoding')
    def _validate_encoding(self, encoding: str):
        """Validates is passed `encoding` literal corresponds suypported encooding."""

        # Try to find encoding
        try:
            codecs.lookup(encoding)

        # Raise `ValidationError` if encoding not found
        except LookupError:
            raise ValidationError(f"Encoding '{encoding}' is invalid or not supported.", field_name='encoding')

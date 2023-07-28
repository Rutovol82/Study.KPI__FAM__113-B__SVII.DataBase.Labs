from functools import partial

from marshmallow import Schema, post_load
from marshmallow.fields import Field, Str, Dict, Nested

from ._base import FileInfoSchema, MarkupFileInfoSchema
from . import SourceSpecificsSchema


# noinspection PyTypeChecker
class ConfigSourceSchema(Schema):
    """Injection config file sources definition modules `marshmallow` `Schema`."""

    file = Nested(FileInfoSchema)
    """Source data file info section."""

    properties = Dict(Str(), Field(), required=False)
    """Dictionary of additional properties, not included to source but exists and common for all of it's rows."""

    specifics = Nested(SourceSpecificsSchema, required=False)
    """Local source specifics section - has priority over the standalone file specifics if also defined."""

    specifics_file = Nested(partial(MarkupFileInfoSchema, markups_valid='supported_markups'),
                            required=False, data_key='specifics-file')
    """Standalone source specifics file definition."""

    @post_load
    def __assemble_data(self, data, **__):
        """Assembles resulting data dictionary."""

        # Pop `specifics_file` (if exists) from `data` to separate variable
        specifics_file = data.pop('specifics_file', None)

        # Create `source_data` dictionary from `specifics` (if provided) or empty
        source_data = data.pop('specifics', None) or dict()

        # Merge `file` section into existing `source_data.file` if needed
        if 'file' in source_data:
            source_data['file'].update(data.pop('file'))

        # Move update `source_data` with all keys remaining in `data`
        source_data.update(data)

        return source_data, specifics_file

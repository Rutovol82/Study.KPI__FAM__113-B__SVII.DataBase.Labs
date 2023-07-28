from marshmallow import Schema, post_load, validate
from marshmallow.fields import Str, Dict, Nested

from . import RootOptionsSchema, ConfigSourceSchema


# noinspection PyTypeChecker
class RootConfigSchema(Schema):
    """Injection config file root-level `marshmallow` `Schema`."""

    id = Str(validate=validate.Length(min=1, max=100))
    """Unique (for target database) name for current injection."""

    sources = Dict(Str(), Nested(ConfigSourceSchema))
    """Sources definition section."""

    options = Nested(RootOptionsSchema, required=False)
    """Injection options. Corresponds to `inject.Options`."""

    @post_load
    def _extract_sources(self, data, **__):
        """Instantiates `csv_inject.Config` object & extracts sources data."""

        # Extract sources data
        sources_data = data.pop('sources')

        return data, sources_data

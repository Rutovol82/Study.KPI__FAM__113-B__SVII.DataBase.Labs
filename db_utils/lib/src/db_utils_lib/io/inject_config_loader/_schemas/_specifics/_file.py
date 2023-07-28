from marshmallow import Schema, post_load
from marshmallow.fields import Str, Field, Dict, Nested

from db_utils_lib.std_utils import FrozenParams

from . import SpecificsTypingSchema, SpecificsTreatmentSchema


# noinspection PyTypeChecker
class SpecificsFileSchema(Schema):
    """Source specifics standalone file / local section `file` section `marshmallow` `Schema`."""

    csv_opts = Dict(Str(), Field(), required=False, data_key='csv-opts')
    """Options dict to be passed to `csv.reader`."""

    @post_load
    def _assemble_csv_opts_data(self, data, **__):
        """Instantiates `csv_opts` `FrozenParams` object (if not None)"""

        csv_opts_data = data.get('csv_opts')
        if csv_opts_data is not None:
            data['csv_opts'] = FrozenParams(kwargs=data['csv_opts'])

        return data

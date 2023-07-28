from marshmallow import Schema, validate, post_load
from marshmallow.fields import Int

from db_utils_lib.db.csv_inject import Options


class RootOptionsSchema(Schema):
    """Injection config file `options` section `marshmallow` `Schema`."""

    atom_size = Int(validate=validate.Range(min=1), data_key='atom-size')
    """Amount of records to be inserted by one transaction."""

    @post_load
    def _init_options(self, data, **__):
        """Instantiates `csv_inject.Options` object."""

        return Options(**data)

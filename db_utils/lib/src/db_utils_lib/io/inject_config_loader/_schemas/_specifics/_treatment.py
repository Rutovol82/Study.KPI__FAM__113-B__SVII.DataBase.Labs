from marshmallow import Schema, validate, post_load
from marshmallow.fields import Str, Dict, List

from db_utils_lib.std_utils import MultiMatch, MultiSub, as_mapper


# noinspection PyTypeChecker
class SpecificsTreatmentSchema(Schema):
    """Source specifics standalone file / local section `treatment` section `marshmallow` `Schema`."""

    cols_names = List(Str(), required=False, data_key='cols-names')
    """
    Names for source columns. 

    **NOTE**: If defined first row of source will be recognized as a data record.
    To avoid set `Source.file.skip_head` to `True`.
    """

    cols_drop = List(Str(), required=False, data_key='cols-drop')
    """
    Collection of columns names to be dropped from the handling (empty set be default).
    """

    cols_extra = Str(validate=validate.OneOf(['keep', 'drop']), required=False, data_key='cols-extra')
    """
    Mode defines behavior about 'extra' columns.
    
      Literal that can take next values:
      
        * '`keep`' - keep extra columns (names will match columns names) - default
        * '`drop`' - drop extra columns
    """

    cols_format_map = List(List(Str(), validate=validate.Length(equal=2)),
                           required=False, data_key='cols-format-map')
    """
    Initialization inputs for the `inject.Source.cols_format_map` `ContentMapper` 
    based onto `MultiSub` - will be used for mapping columns names onto properties names.
    """

    vals_format_map = Dict(Str(), List(List(Str(), validate=validate.Length(equal=2))),
                           required=False, data_key='vals-format-map')
    """
    Initialization inputs for the `inject.Source.vals_format_map` `ContentMapper` 
    based onto `MultiMatch` mapping and maps properties names onto `MultiSub` formatters instances. 
    """

    @post_load
    def _cast_cols_drop(self, data, **__):
        """Casts `cols_drop` (if provided) into Python `set`."""

        cols_drop = data.get('cols_drop')
        if cols_drop is not None:
            data['cols_drop'] = set(cols_drop)

        return data

    @post_load
    def _init_cols_format_map(self, data, **__):
        """Instantiates `cols_format_map` mapper object (if not None)"""

        cols_format_map_data = data.get('cols_format_map')
        if cols_format_map_data is not None:
            data['cols_format_map'] = as_mapper(MultiSub.from_iter(cols_format_map_data))

        return data

    @post_load
    def _init_vals_format_map(self, data, **__):
        """Instantiates `vals_format_map` mapper object (if not None)"""

        vals_format_map_data = data.get('vals_format_map')
        if vals_format_map_data is not None:
            data['vals_format_map'] = \
                as_mapper(
                    MultiMatch.from_iter(
                        (
                            (match, MultiSub.from_iter(inputs))
                            for match, inputs in vals_format_map_data.items()
                        ),
                        fullmatch=True
                    ),
                    except_fail=(ValueError,)
                )

        return data

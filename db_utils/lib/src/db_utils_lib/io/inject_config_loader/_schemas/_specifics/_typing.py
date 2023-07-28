from marshmallow import Schema, post_load
from marshmallow.fields import List, Dict, Str

from db_utils_lib.std_utils import MultiMatch, as_mapper
from db_utils_lib.db.csv_inject import DEFAULT_CSV_TYPER


class SpecificsTypingSchema(Schema):
    """Source specifics standalone file / local section `typing` section `marshmallow` `Schema`."""

    null_alias = List(Str(), required=False, data_key='null-alias')
    """
    List of `null` value string alias - will be used to create `TexTyper` for current injection.
    """

    types_map = Dict(Str(), Str(), data_key='types-map')
    """
    Initialization inputs for the `inject.Config.types_map` `Mapping` 
    based onto `MultiMatch` mapping and maps properties names onto corresponding typekeys. 
    """

    @post_load
    def _assemble_map_assemble_handler(self, data, **__):
        """Assembles `types_map` `ContentMapper` and `types_handler` `textypes.HandlerABC` instances."""

        # Assemble `types_map` mapper
        types_map = as_mapper(MultiMatch.from_iter(data.pop('types_map').items(), fullmatch=True))

        # Assemble `types_handler`
        if 'null_alias' in data:
            types_handler = DEFAULT_CSV_TYPER.new_derived(null_alias=data['null_alias'], strict_type_match=False)
        else:
            types_handler = DEFAULT_CSV_TYPER

        # Pack assembled instances into kwargs dict and return
        return dict(types_map=types_map, types_handler=types_handler)

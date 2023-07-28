from db_utils_lib.typetools.textyper import TexTyper, types


DEFAULT_CSV_TYPER = TexTyper.new(types.INT, types.FLOAT, types.DECIMAL, types.BOOL, types.STR,
                                 null_alias=('null', 'NULL'),
                                 strict_type_match=False)
"""
Default `TypeRegister` for csv injection operations. 
(In purpose to minimize setups :)
"""

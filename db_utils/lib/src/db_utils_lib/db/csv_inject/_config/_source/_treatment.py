from dataclasses import dataclass, field
from collections.abc import Callable, Sequence, Collection

from functools import partial
from typing import Literal

from db_utils_lib.std_utils import ContentMapper, as_mapper


@dataclass(frozen=True)
class SourceTreatment:
    """Dataclass for storing db injection source data treatment options."""

    cols_names: Sequence[str] = None
    """
    Names for source columns.
    
      **NOTE**: If column name will be set as `None` - this column will be excluded.  
    
        **NOTE**: If defined first row of source will be recognized as a data record.
        To avoid set `Source.file.skip_head` to `True`.
    """

    cols_drop: Collection[str] = field(default_factory=set)
    """
    Collection of columns names to be dropped from the handling (empty set be default).

      **NOTE**: Passed collection will not be transformed so it is recommended to use `set` 
      as a `cols_drop` collection in purpose to increase performance.
    """

    cols_extra: Literal['keep', 'drop'] = 'keep'
    """
    Mode defines behavior about 'extra' columns.
    
      Literal that can take next values:
      
        * '`keep`' - keep extra columns (names will match columns names) - default
        * '`drop`' - drop extra columns
    """

    cols_format_map: ContentMapper[str, str] = field(default_factory=partial(as_mapper, 'exact'))
    """
    `ContentMapper` to be used for producing mapping of source columns on target properties names.

      **NOTE**: Behavior for the unmatched ('extra') columns will be defined by 
    """

    vals_format_map: ContentMapper[str, Callable[[str], str]] = \
        field(default_factory=partial(as_mapper, lambda str_: str_, as_const=True))
    """
    `ContentMapper` to be used for producing mapping of properties names onto formatting callables.

      **NOTE**: Unmatched properties values will be leaved as it is.
    """

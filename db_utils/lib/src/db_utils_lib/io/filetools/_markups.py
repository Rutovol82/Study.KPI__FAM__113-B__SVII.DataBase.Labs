from collections.abc import Iterable, Mapping
from os import PathLike
from pathlib import Path
from types import MappingProxyType


class MarkupsSimplets:
    """
    Class provides some very simple tools to help in
    file markup recognition by its path.
    """

    # ------ Protected fields & public properties

    _alias: dict[str, str]      # Dictionary of known markups (values) and their alias (keys)

    @property
    def known_alias(self) -> Mapping[str, str]:
        """Returns mapping of known markups alias (keys) and names (values)."""

        return MappingProxyType(self._alias)

    @property
    def known_names(self) -> set[str]:
        """Returns `set` of known markups names."""

        return set(self._alias.values())

    # ------ Instantiation methods

    def __init__(self, alias_mapping: Mapping[str, str] | Iterable[tuple[str, str]] = None, *, copy=True):
        """
        Initializes new instance of `MarkupsSimplets` class.

        :param alias_mapping: initial mapping of known markups (values) and their alias (keys)
        """

        self._alias = (dict(alias_mapping) if alias_mapping is not None else dict()) if copy else alias_mapping

    # ------ Functionality methods

    def markup_from_path(self, path: str | PathLike[str]) -> tuple[str, bool] | tuple[None, None]:
        """
        Tries to extract file markup from its path.

          Returns:

          * (name, True) - if markup extracted & known
          * (lower-case path suffix without dot, False) - if extension extracted, but unknown
          * (None, None) - if extension not exists
        """

        # Extract file path suffix
        suffix = Path(path).suffix

        # Check length - if 0 - it's not an extension - return None, None
        if len(suffix) == 0:
            return None, None

        # Extract possible markup
        markup = suffix[1:].lower()

        # Handle it using alias dict
        if markup is self._alias:
            markup, known = self._alias[markup], True
        else:
            known = False

        return markup, known


markups = MarkupsSimplets({'json': 'json', 'yaml': 'yaml', 'yml': 'yaml'}, copy=False)
"""
Default global instance of `MarkupsSimplets` - exists in purpose to be used as primary functions set.

  Supported markups/alias:

  * `yaml`: '`yaml`' / '`yml`'
  * `json`: '`json`'
"""

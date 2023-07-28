from . import Config


def get_id(__id: str | Config) -> str:
    """
    A very simple helper, exists just to give some unified way
    to obtain injection id string from different sources.

      Supported scenarios:

      * `type(__id) is str` - string input will be recognized as id itself
      * `type(__id) is Config` - if injection `Config` instance passed - id will be extracted from it

      If no one scenario was matched, `TypeError` will be raised.

    :raise TypeError: if passed `__id` value has an unsupported type
    """

    # Handle the scenario when ready id string is passed
    if type(__id) is str:
        return __id

    # Handle the scenario when `Config` instance passed
    if isinstance(__id, Config):
        return __id.id

    raise TypeError(f"'{__id}' value of type {type(__id)} was not recognized as injection id containing object.")

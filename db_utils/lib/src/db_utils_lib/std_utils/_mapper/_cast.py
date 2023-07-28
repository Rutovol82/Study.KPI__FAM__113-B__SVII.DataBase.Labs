from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal

from . import ContentMapper, EmptyMapper, ExactMapper, ExternMapper, DictMapper


def as_mapper(arg: Mapping[Any, Any] | Callable[[Any], Any] | Literal['exact'] | Any | None = None,
              *,
              as_const: bool = False,
              except_fail: Iterable[type[BaseException]] | BaseException = None) -> ContentMapper[Any, Any]:
    """
    Tries to wrap passed object into `ContentMapper` interface.

      Supports many modes of wrapping depends on passed arguments:

        * `arg is None`

          If `None` value passed as arg will produce empty mapper instance.

        * `arg == 'exact'`

          If `arg` is a literal `'exact'`, will produce mapper, always maps inputs onto themselves.

        * `as_const == True`

          If argument `as_const` set to True, will produce mapper, always maps inputs onto `arg` value.

        * `arg is Callable`

          If `arg` is `Callable`, will produce mapper, wraps it to transform values.

          To be supported callable must have the next signature: `callable(key_) -> value_`

          In case of operation fail, callable must produce an exception of any type.
          Types of possibly produced exceptions must be passed through the `except_fail` argument.

          **NOTE**: Can be used as decorator, but it's not recommended because of total replacement of original object
          without saving its attributes.

        * `arg is Mapping`

          If `arg` implementing `collections.abc.Mapping`, will produce mapper, wraps it to transform values.
    """

    if arg is None:
        return EmptyMapper()

    if arg == 'exact':
        return ExactMapper()

    if as_const:
        return ExternMapper(lambda _: arg)

    if isinstance(arg, Callable):
        exceptions =                                                                \
            tuple() if except_fail is None                                          \
            else tuple(except_fail) if not isinstance(except_fail, BaseException)   \
            else except_fail
        return ExternMapper(arg, except_fail=exceptions)

    elif isinstance(arg, Mapping):
        return DictMapper(arg)

    else:
        raise TypeError(f"Unsupported argument type {type(arg)}")

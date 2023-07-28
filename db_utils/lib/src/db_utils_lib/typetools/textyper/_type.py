from collections.abc import Callable
from typing import TypeVar

from . import TexTypeABC


TP_ = TypeVar('TP_')


class TexType(TexTypeABC[TP_]):
    """
    Abstraction used in `TexTyper` to handle stored types.

    To instantiate use inheritance or initialize `TexType` instance with your values.
    """

    # ------ Protected fields & public properties

    _key: str       # textype typekey
    _type: type     # TexType equivalent Python type

    _match: Callable[[str], bool]   # Callable, checks if string matches current textype

    _dump: Callable[[TP_], str]     # Callable, converts Python object corresponds current TexType into string.
    _load: Callable[[str], TP_]     # Callable, converts string value of current TexType into equivalent Python object.

    # ------ Instantiation methods

    def __init__(self, key_: str, type_: type,
                 dump_func: Callable[[TP_], str] = None,
                 load_func: Callable[[str], TP_] = None,
                 match_func: Callable[[str], bool] = None):
        """
        Initializes new instance of `TexType` class.

          Instantiates `TexTypeABC` instance based on passed functions and values -
          without need to define own derived class.

            **NOTE**: Passed callables must accept the next rules:

            * `dump_func`

              + Must have signature: `(Any) -> str`
              + Must raise `ValueError` on fail

            * `load_func`

              + Must have signature: `(str) -> Any`
              + Must raise `ValueError` on fail

            * `match_func`

              + Must have signature: `(str) -> bool`
              + Must NOT raise exceptions

        :param key_: textype typekey
        :param type_: textype equivalent Python type
        :param dump_func: callable, checks if string matches current textype
        :param load_func: callable, converts Python object corresponds current TexType into string
        :param match_func: callable, converts string value of current TexType into equivalent Python object
        """

        self._key = key_
        self._type = type_
        self._dump = dump_func
        self._load = load_func
        self._match = match_func

    # ------ Abstract (and not) interface methods

    @property
    def key(self) -> str:
        """TexType typekey."""
        return self._key

    @property
    def type(self) -> type:
        """TexType equivalent Python type."""
        return self._type

    # noinspection PyMethodMayBeStatic
    def match(self, str_: str) -> bool:
        """Checks if `str_` matches current TexType."""

        return self._match(str_) if self._match is not None else super().match(str_)

    def load(self, str_: str) -> TP_:
        """
        Converts raw string value of current TexType into equivalent Python object.

        :raise ValueError: if unable to load value or values load not supported.
        """

        return self._load(str_) if self._load is not None else super().load(str_)

    def dump(self, val_: TP_) -> str:
        """
        Converts Python object corresponds current TexType into equivalent string represent.

        :raise ValueError: if unable to dump value or values dump not supported.
        """

        return self._dump(val_) if self._dump is not None else super().dump(val_)

    # ------ Python service methods overloads

    def __str__(self):
        return self.key

    def __repr__(self):
        return f"<{self.__class__.__name__}: '{self}'>"

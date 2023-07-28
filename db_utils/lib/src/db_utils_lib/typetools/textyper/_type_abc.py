from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic


TP_ = TypeVar('TP_')


class TexTypeABC(Generic[TP_], metaclass=ABCMeta):
    """
    Abstraction used in `TexTyper` to handle stored types.

    To instantiate use inheritance or initialize `TexType` instance with your values.
    """

    # ------ Abstract (and not) interface methods

    @property
    @abstractmethod
    def key(self) -> str:
        """TexType typekey."""
        pass

    @property
    @abstractmethod
    def type(self) -> type:
        """TexType equivalent Python type."""
        pass

    # noinspection PyMethodMayBeStatic
    def match(self, str_: str) -> bool:
        """Checks if `str_` matches current textype."""

        # Default implementation just always returns False
        return False

    def load(self, str_: str) -> TP_:
        """
        Converts raw string value of current textype into equivalent Python object.

        :raise ValueError: if unable to load value or values load not supported.
        """

        # Default implementation just always raise ValueError
        raise ValueError(f"{self} not support values load.")

    def dump(self, val_: TP_) -> str:
        """
        Converts Python object corresponds current textype into equivalent string represent.

        :raise ValueError: if unable to dump value or values dump not supported.
        """

        # Default implementation just always raise ValueError
        raise ValueError(f"{self} not support values load.")

    # ------ Python service methods overloads

    def __str__(self):
        return self.key

    def __repr__(self):
        return f"<{self.__class__.__name__}: '{self}'>"

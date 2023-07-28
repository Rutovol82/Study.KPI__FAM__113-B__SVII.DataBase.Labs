from typing import TypeVar
from collections.abc import Callable

from . import ContentMapper


TKey_ = TypeVar('TKey_')
TValue_ = TypeVar('TValue_')


class ExternMapper(ContentMapper):
    """
    Content mapper wrapper for callables.

      Build `ContentMapper` interface around callable with the next signature:

        `callable(key_: TKey_) -> TValue_`

          **NOTE**: Can be used as decorator, but it's not recommended because of total replacement of original object
          without saving its attributes.

          **NOTE**: It is recommended to use `as_mapper()` function to create `ExternMapper` instances
          instead of direct `ExternMapper` instantiation.
    """

    # ------ Protected fields

    _transformer: Callable[[TKey_], TValue_]    # Keys transformation callable
    _except_fail: tuple[type[BaseException]]    # Tuple of exceptions types, indicates transformation fail

    # ------ Instantiation methods

    def __init__(self, transformer: Callable[[TKey_], TValue_], except_fail: tuple[type[BaseException]] = None):
        """
        Initializes new instance of `ExternMapper` class.

        :param transformer: callable to be used to transform values, must have the next signature:
                            `callable(key_: TKey_) -> TValue_`
        :param except_fail: tuple of exceptions types, that can be raised by transformer
                            as a sign that the conversion is not possible
        """

        self._transformer = transformer
        self._except_fail = except_fail if except_fail is not None else tuple()

    # ------ Functionality methods

    def get_match(self, key: TKey_) -> TValue_:

        try:
            return self._transformer(key)

        # If transformation failed, the transformer must raise one of the exceptions passed by `except_fail`.
        # So `get_match()` method trying to catch those exceptions to reraise `ValueError`, specified by its docs.
        except self._except_fail as e:
            raise ValueError(*e.args) from e

    def try_get_match(self, key: TKey_, default: TValue_ = None) -> TValue_:

        try:
            return self._transformer(key)

        # If transformation failed, the transformer must raise one of the exceptions passed by `except_fail`.
        # So `get_match()` method trying to catch those exceptions to return default value.
        except self._except_fail:
            return default

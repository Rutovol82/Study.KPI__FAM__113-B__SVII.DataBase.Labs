from inspect import Parameter, Signature, signature, isclass
from typing import Callable, Type, Any, get_args
from types import UnionType


# Define public visible members
__all__ = ['sig_inspect', 'sig_inspect_extension']


# noinspection PyPep8Naming
class sig_inspect:
    """
    Class, helps to perform inspection operations over callables signatures.

      The current class is a simple container, contains links to original callable, and its signature.

        All inspection functionality is extensible and defined by different
        classes, derived from `sign_inspect_extension` class.
    """

    _callable: Callable     # Source callable object
    _signature: Signature   # Source callable object signature

    @property
    def signature(self) -> Signature:
        """Source callable signature."""
        return self._signature

    @property
    def callable(self) -> Callable:
        """Source callable."""
        return self._callable

    def __init__(self, callable_obj: Callable, sig: Signature = None):
        """
        Initializes new instance of `sig_inspect` class for a given callable object
        and (optionally) it`s signature (`sig` parameter) - if not given - will be obtained automatically.

        :param callable_obj: Source callable object
        :param sig: source callable object signature (optional - will be obtained automatically if not provided)
        """

        self._callable = callable_obj
        self._signature = sig if sig is not None else signature(callable_obj)

    @property
    def index_param(self):
        """Extension for parameters indexation."""
        return index_param(self)

    @property
    def get_arg(self):
        """Extension for arguments extraction."""
        return get_arg(self)


# noinspection PyPep8Naming
class sig_inspect_extension:
    """Base class for `sig_inspect` extensions."""

    _source: sig_inspect

    @property
    def source(self):
        return self._source

    def __init__(self, source: sig_inspect):
        self._source = source


# noinspection PyPep8Naming
class index_param(sig_inspect_extension):
    """`sig_inspect` extension for parameters indexation."""

    def try_by_type(self, tp: Type, default: Any = None) -> Parameter:
        """
        Helps to get first parameter from signature, annotated by `tp` type.

          Returns `default` value if not found.

        :param tp: target parameter type
        :param default: default value to be returned if target parameter not found
        :return: target parameter or `default` if not found
        """

        def predicate(item):
            annotation = item.annotation
            return annotation is tp or (isclass(annotation) and issubclass(annotation, tp))

        return next(filter(predicate, self.source.signature.parameters.values()), default)

    def by_type(self, tp: Type) -> Parameter:
        """
        Helps to get first parameter from signature, annotated by `tp` type.

          Raises `TypeError` if not found.

        :raise TypeError: if parameter not found
        :param tp: target parameter type
        :return: target parameter or `default` if not found
        """

        param = self.try_by_type(tp=tp, default=None)

        if param is None:
            raise TypeError(f"Decorated function '{self.source.callable.__name__}' "
                            f"takes no arguments of accepted type '{tp}'.")

        return param


# noinspection PyPep8Naming
class get_arg(sig_inspect_extension):
    """`sig_inspect` extension for arguments extraction."""

    def try_by_name(self, arg_name: str, default: Any, /, *args, **kwargs):
        """
        Helps to extract argument value by it`s name from passed args & kwargs.

          Returns `default` value if not found.

        :param arg_name: target argument name
        :param default: default value to be returned if target argument not found
        :return: target argument value or `default` if not found
        """

        bound = self.source.signature.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        return bound.arguments.get(arg_name, default)

    def by_name(self, arg_name: str, /, *args, **kwargs):
        """
        Helps to extract argument value by it`s name from passed args & kwargs.

          Raises `ValueError` if not found.

        :raise ValueError: if argument not found
        :param arg_name: target argument name
        :return: target argument value
        """

        bound = self.source.signature.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        if arg_name in bound.arguments:
            return bound.arguments[arg_name]

        raise ValueError(f"Argument '{arg_name}' not passed.")

from abc import ABCMeta
from collections.abc import Iterable, Mapping, Sequence
from types import MappingProxyType
from typing import Any

from . import Parameterizable


# Define public visible members
__all__ = ['Params', 'params', 'FrozenParams', 'frozen_params']


# ------ `Params` base class implements common functionality

class _ParamsBase(Parameterizable, metaclass=ABCMeta):
    """
    Base class for `Params` & `FrozenParams`.
    Defines common service methods.
    """

    _args: Any      # Protected field to store args
    _kwargs: Any    # Protected field to store kwargs

    def __str__(self):
        return f"{self.__class__.__name__}(args={str(self._args)}, kwargs={str(self._kwargs)})"

    def __repr__(self):
        return self.__str__()


# ------ 'Mutable' `Params` class & instantiation helper function

class Params(_ParamsBase):
    """Class to store args & kwargs."""

    @property
    def args(self) -> Sequence[Any]:
        return self._args

    @property
    def kwargs(self) -> Mapping[str, Any]:
        return self._kwargs

    def __init__(self, args: Sequence[Any] = None, kwargs: Mapping[str, Any] = None):
        self._args = args if args is not None else tuple()
        self._kwargs = kwargs if kwargs is not None else dict()


def params(*args, **kwargs) -> Params:
    """Initializes new instance of `Params` class."""

    return Params(args=list(args), kwargs=kwargs)


# ------ 'Immutable' `Params` class & instantiation helper function

class FrozenParams(_ParamsBase):
    """Class to store args & kwargs in immutable state."""

    @property
    def args(self) -> Sequence[Any]:
        return tuple(self._args) if type(self._args) is not tuple else self._args

    @property
    def kwargs(self) -> Mapping[str, Any]:
        return MappingProxyType(self._kwargs)

    def __init__(self, args: Iterable[Any] = None, kwargs: Mapping[str, Any] = None):
        self._args = args if args is not None else tuple()
        self._kwargs = kwargs if kwargs is not None else dict()


def frozen_params(*args, **kwargs) -> FrozenParams:
    """Initializes new instance of `FrozenParams` class."""

    return FrozenParams(args=args, kwargs=kwargs)

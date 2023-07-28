from abc import ABCMeta, abstractmethod
from collections.abc import Sequence, Mapping
from typing import Any, Callable


class Parameterizable(metaclass=ABCMeta):
    """
    Abstraction, defines support of two properties - `arg` & `kwargs`,
    designed to return args & kwargs for some callable.
    """

    @property
    @abstractmethod
    def args(self) -> Sequence[Any]:
        """Positional arguments sequence (`args`)."""
        pass

    @property
    @abstractmethod
    def kwargs(self) -> Mapping[str, Any]:
        """Keyword arguments mapping (`kwargs`)."""
        pass

    def pass_to(self, callable_obj: Callable, /, *args, **kwargs):
        """
        Uses stored args & kwargs to call some callable object.

          Additional args & kwargs will be passed after stored if provided.

        :param callable_obj: object to be called
        :param args: additional args
        :param kwargs: additional kwargs
        :return: call's return
        """

        return callable_obj(*self.args, *args, **self.kwargs, **kwargs)

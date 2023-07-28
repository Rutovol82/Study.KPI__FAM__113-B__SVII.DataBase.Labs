from functools import update_wrapper
from typing import Callable


# Define public visible members
__all__ = ['decorator_builder']


# noinspection PyPep8Naming
class decorator_builder:
    """
    Helper decorator for the decorator builders.

      Allow them to be called as raw decorators (i.e. without arguments).

        To be supported target decorator builder must have an ability to be called without arguments
        (for example, have default values for all args)
    """

    __builder_original__: Callable
    __builder_ismethod__: bool

    def __init__(self, builder_obj: Callable, /, ismethod: bool = False):
        """
        Allow decorator builders to be called as raw decorators (i.e. without arguments).

          To be supported target decorator builder must have an ability to be called without arguments
          (for example, have default values for all args)

        :param ismethod: define is target decorator builder a method or not
        """

        update_wrapper(self, builder_obj)

        self.__builder_original__ = builder_obj
        self.__builder_ismethod__ = ismethod

    @staticmethod
    def method(builder_obj: Callable):
        """
        Allow method-based decorator builders to be called as raw decorators (i.e. without arguments).

          To be supported target decorator builder must have an ability to be called without arguments
          (for example, have default values for all args)
        """

        return decorator_builder(builder_obj, ismethod=True)

    def __call__(self, *args, **kwargs):
        check_arg = 1 if self.__builder_ismethod__ else 0
        if len(args) == check_arg + 1 and len(kwargs) == 0 and callable(args[check_arg]):
            return self.__builder_original__()(args[check_arg])
        return self.__builder_original__(*args, **kwargs)

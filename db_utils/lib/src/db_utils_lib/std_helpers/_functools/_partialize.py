from functools import wraps, partial
from typing import Callable


# Define public visible members
__all__ = ['partialize']


def partialize(callable_obj: Callable):
    """
    Decorator, allows to split callable handling on two-approaches.

      Wraps original callable object into `functools.partial`, so:

      - On first call passed arguments will bw filled with `functools.partial`
      - On second call passed arguments will be filled to first call return and callable will be called.
    """

    @wraps(callable_obj)
    def wrapper(*args, **kwargs):
        return partial(callable_obj, *args, **kwargs)

    return wrapper

import time
from abc import ABCMeta, abstractmethod
from typing import ContextManager

from . import TimerState


class RunTimeMeasurer(ContextManager, metaclass=ABCMeta):
    """
    Contextmanager run time measurer abstraction.

    * Measures run time in seconds.
    * Supports classic and contextmanager modes (recommended option).
    """

    # ------ State properties

    @property
    @abstractmethod
    def state(self) -> TimerState:
        pass

    @property
    def is_stopped(self) -> bool:
        """Returns `True` if timer state is `STOPPED`, otherwise - `False`"""

        # Default implementation checks `state` property
        return self.state == TimerState.STOPPED

    # ------ Time measurements properties & standalone getters

    @property
    @abstractmethod
    def total_time(self) -> float:
        """
        Measured time in milliseconds.

        :raise RuntimeError: if requested from non-`STOPPED` instance
        """
        pass

    def get_total_time(self) -> float | None:
        """
        Returns measured time in milliseconds.

        If invoked before measurement is complete (non-`STOPPED`), returns `None`.
        """

        # Default implementation checks `is_stopped()` property.
        return self.total_time if self.is_stopped else None

    # ------ `start()`/`stop()` abstract methods definition

    @abstractmethod
    def start(self):
        """
        Starts time measurement.

        :raise RuntimeException: if invoked on non-`CREATED` instance
        """

    @abstractmethod
    def stop(self):
        """Stops time measurement and writes measured time."""

    # ------ Contextmanager protocol

    def __enter__(self) -> 'RunTimeMeasurer':

        # Default implementation just invokes `start()` method.
        self.start()

        # Return `self`
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Default implementation just invokes `stop()` method
        self.stop()

    # ------ Additional methods

    # noinspection PyShadowingBuiltins
    def total_time_string(self, format: str = '%H:%M:%S') -> str:
        """
        Returns formated timestring from `total_time`

        :param format: time format string ('Hours:Minutes:Seconds.Milliseconds' by default)
        :raise RuntimeError: if time requested before timer exits
        """

        # Use `time.strftime()` & `time.gmtime()` to format time from seconds
        return time.strftime(format, time.gmtime(self.total_time))

    def __str__(self):
        return f"<{self.__class__.__name__}(state='{self.state}'" \
               f"{f', total_time=[{self.total_time_string()}]' if self.is_stopped else ''})>"

    def __repr__(self):
        return str(self)

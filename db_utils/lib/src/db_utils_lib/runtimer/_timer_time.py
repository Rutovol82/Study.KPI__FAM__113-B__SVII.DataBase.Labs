import time

from . import RunTimerABC, TimerState


# Define public visible members
__all__ = ['RunTimer', 'runtimer']


class RunTimer(RunTimerABC):
    """
    Basic `RunTimerABC` implementation.
    Uses `time` module is used to provide time measurement.
    """

    # ------ Protected fields & public properties

    _start_time: float = None       # Variable stores start time (set after stop)
    _total_time: float = None       # Variable stores total time (set after stop)

    @property
    def state(self) -> TimerState:

        if self._start_time is None:
            return TimerState.CREATED

        elif self._total_time is None:
            return TimerState.RUNNING

        return TimerState.STOPPED

    @property
    def total_time(self) -> float:

        # Raise `RuntimeError` if measurement not finished
        if self._total_time is None:
            raise RuntimeError("Time measurement not finished.")

        return self._total_time

    # ------ `__init__()` method overload

    def __init__(self, name: str = None, *, anonymous: bool = False):
        """
        Initializes new instance of `RunTimer` class.

        :param name: optional timer name
        :param anonymous: whether to register current timer in `timers` registry (`True` by default)
        """

        super().__init__(name=name, anonymous=anonymous)

    # ------ `start()`/`stop()` methods

    def start(self):

        # Raise `RuntimeError` if invoked on the second time
        if self._start_time is not None:
            raise RuntimeError("Time measurement is already started.")

        self._start_time = time.time()

    def stop(self):

        end_time = time.time()
        self._total_time = end_time - self._start_time


def runtimer(name: str = None, *, anonymous: bool = False):
    """
    Creates new instance of `RunTimer` class.

    :param name: optional timer name
    :param anonymous: whether to register current timer in `timers` registry (`True` by default)
    """

    return RunTimer(name=name, anonymous=anonymous)

from enum import Enum

# Define public visible members
__all__ = ['TimerState', 'CREATED', 'RUNNING', 'STOPPED']


class TimerState(str, Enum):
    """Enumeration represents `RunTimerABC` run timers states."""

    CREATED = 'created'
    """Timer created but not strated."""

    RUNNING = 'running'
    """Timer is running now."""

    STOPPED = 'stopped'
    """Timer stopped."""


CREATED = TimerState.CREATED
RUNNING = TimerState.RUNNING
STOPPED = TimerState.STOPPED

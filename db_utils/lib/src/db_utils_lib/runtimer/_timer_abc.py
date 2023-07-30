from abc import ABCMeta

from . import RunTimeMeasurer, timers


class RunTimerABC(RunTimeMeasurer, metaclass=ABCMeta):
    """
    Contextmanager runtime timer abstraction, extends `RunTimeMeasurer`

      Additional functionality:

      * Each timer can have a name or unique identifier (see `name` & `id` properties)
      * Each timer will be automatically registered in the global `timers` registry.
    """

    # ------ Setup protected fields & public properties

    _timer_id: str          # Timer id string
    _timer_name: str        # Optional timer name

    @property
    def name(self) -> str | None:
        """Returns timer or `None` (if name not set)."""

        return self._timer_name

    @property
    def id(self) -> str:
        """
        Timer id that will be used for registering in timers registry (for **not-anonymous** timers)
        or just match timer `name` (for **anonymous**).

          Behavior:

          * if timer is not **anonymous** - will match `name` property if provided
            or be a combination of `name` and some addition (if timer with this name already exists) -
            else will be set to a random identifier
          * if timer is **anonymous** - will match `name` property if provided -
            else will be `None` as same as `name`
        """

        return self._timer_id

    # ------ `__new__()` & base `__init__()` methods

    def __init__(self, name: str = None, *, anonymous: bool = False):
        """
        Provides basic `RunTimerABC` initialization.

        :param name: optional timer name
        :param anonymous: whether to register current timer in `timers` registry (`True` by default)
        """

        self._timer_name = name

        # If not anonymous - register in `timers`
        if not anonymous:
            self._timer_id = timers.register(timer=self, name=name, on_dupl='resolve')
        # Else default `id` to `name`
        else:
            self._timer_id = name

    # ------ `__str__()` overload

    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', state={self.state.upper()}" \
               f"{f', total_time=[{self.total_time_string()}]' if self.is_stopped else ''})>"

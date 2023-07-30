import uuid
from typing import Mapping, Literal
from types import MappingProxyType

from db_utils_lib.std_helpers import Singleton

from . import RunTimeMeasurer, TimerState


# Define public visible members
__all__ = ['TimersRegistry', 'timers']


class TimersRegistry(Singleton):
    """
    Class represents global run-timers registry, singleton.

      It's only instance collects links to all created `RunTimerABC`
      derived classes instances (except it is prevented explicitly).

        Also provided ability to manually register any `RunTimeMeasurer`
        derived classes instances.
    """

    # ------ Protected fields & public properties

    _registered: dict[str, RunTimeMeasurer]     # Dictionary holds all registered timers

    @property
    def registered(self) -> Mapping[str, RunTimeMeasurer]:
        """Registered timers mapping."""
        return MappingProxyType(self._registered)

    # ------ Instantiation methods

    def __init__(self):
        """Initializes only instance of `TimersRegistry` class."""

        self._registered = dict()

    # ------ Access methods

    def filter(self, *states: TimerState, ex: bool = False) -> Mapping[str, RunTimeMeasurer]:
        """
        Returns copy of mapping of currently registered instances,
        filtered by `states`:

        * if `ex` is `False` (default option) - includes only timers with `state` in `states`
        * if `ex` is `True` - includes only timers with `state` NOT in `states`

        :param states: filtering states (`TimerState`)
        :param ex: exclude timers with `state` in `states` instead of include

        :return: filtered copy of `registered` mapping
        """

        if ex:
            filtered = {id_: timer for id_, timer in self._registered.items() if timer.state not in states}
        else:
            filtered = {id_: timer for id_, timer in self._registered.items() if timer.state in states}

        return filtered

    def __getitem__(self, id_: str):
        return self._registered[id_]

    def __iter__(self):
        return iter(self._registered)

    # ------ Registration method

    def register(self,
                 timer: RunTimeMeasurer, name: str = None,
                 on_dupl: Literal['except', 'ignore', 'resolve'] = 'resolve') -> str | None:
        """
        Registers new timer in the register.

          ----

        If `name` not provided (not passed or passed `None`), random identifier will be generated.

          ----

        Behavior in case of duplicate name can be defined by the `on_dupl` literal.
        It can take the next values:

        * '`except`' - if `name` already exists, raise `KeyError`
        * '`ignore`' - if `name` already exists, do nothing - `None` will be returned instead of id in that case
        * '`resolve`' - if `name` already exists, passed name will be modified to be unique (default option)

          ----

        :param timer: timer object to register
        :param name: timer registration name
        :param on_dupl: duplicate names resolution mode literal

        :raise KeyError: if `name` already exists and `on_dupl` is '`except`'

        :return: final registration id
        """

        # Handle case when name not passed
        if name is None:

            id_ = str(uuid.uuid4())
            self._registered[id_] = timer

            return id_

        # Resolve duplicate name according to `on_dupl`
        while name in self._registered:

            if on_dupl == 'resolve':
                name += '*'
                continue

            if on_dupl == 'except':
                raise KeyError(f"Timer with name {name} already exists.")

            if on_dupl == 'ignore':
                return None

        # Set by `name`
        self._registered[name] = timer
        return name


timers = TimersRegistry()
"""Global run-timers registry"""

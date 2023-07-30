from collections.abc import Iterable, Sequence, Mapping, Callable
from functools import partial, update_wrapper
from typing import Any

from argparse import ArgumentParser


# Define public visible members
__all__ = ['db_utils_command']


# noinspection PyPep8Naming
class db_utils_command:
    """
    Class, represents `db_utils` command.

      Must be used as a wrapper for the command script entry point callable.

        The recommended way to instantiate this class - use `entry_point()` decorator method.

          ----

    **INFO**: According to contract, entry point callable attribute must have name `__command__`
    and signature similar to the next:

      `entry_point(dumper: db_utils_lib.db.wrapper.Dumper, **kwargs)`

        Here `**kwargs` are arguments, described in `args` during `db_utils_command` creation
        or passed by `argsetup` method.
    """

    # ------ Protected fields

    _command: str               # Command name
    _description: str           # Command description

    _callable_entry: Callable                       # Command entry point callable
    _argsetup: Callable[[ArgumentParser], None]     # Command `argparse` subparser setup function

    # ------ Instantiation methods

    def __init__(self, entry_callable: Callable, /,
                 command: str, description: str = None,
                 argsetup: Callable[[ArgumentParser], None] = None):
        """
        Initializes new instance of `db_utils_command` class.

          **WARNING**: This is a service method by design.
          It is highly recommended to use `new()` method instead.

        :param entry_callable: command entry point callable
        :param command: command name - will be used as command to activate current subcommand
        :param description: command description - will be displayed in current subcommand help
        :param argsetup: command `argparse` subparser setup function
        """

        update_wrapper(self, entry_callable)

        self._command = command
        self._description = description

        self._callable_entry = entry_callable
        self._argsetup = argsetup

    @classmethod
    def new(cls, entry_callable: Callable,
            command: str, description: str = None,
            argsetup: Callable[[ArgumentParser], None] = None,
            args: Iterable[Sequence[Iterable[str] | str, Mapping[str, Any]]] = None) -> 'db_utils_command':
        """
        Initializes new instance of `db_utils_command` class.

        :param entry_callable: command entry point callable
        :param command: command name - will be used as command to activate current subcommand
        :param description: command description - will be displayed in current subcommand help
        :param argsetup: command `argparse` subparser setup function (for fast setup - use `args` param instead)
        :param args: options for the command subparser arguments (`argsetup` will be generated automatically)

        :return: initialized instance of `db_utils_command` class
        """

        # Handle `argsetup` & `args` input
        if argsetup is None:
            # Build `argsetup` based on `args` if `argsetup` is not provided or stub func if `args` not provided also
            argsetup = cls._build_argsetup(args) if args is not None else lambda _: None

        # Initialize and return new instance of `db_utils_command`
        return cls(entry_callable, command=command, description=description, argsetup=argsetup)

    # ------ Properties getters, `__call__` & `setup_parser` methods

    @property
    def command(self):
        """Command name."""
        return self._command

    @property
    def description(self):
        """Command description."""
        return self._description

    def __call__(self, *args, **kwargs):
        # On call - recalls wrapped callable entry
        return self._callable_entry(*args, **kwargs)

    def setup_parser(self, parser: ArgumentParser):
        """Sets up all necessary arguments for command `argparse` subparser."""
        self._argsetup(parser)

    # ------ Decorator methods

    @classmethod
    def entry_point(cls, command: str, description: str = None,
                    argsetup: Callable[[ArgumentParser], None] = None,
                    args: Iterable[Sequence[Iterable[str] | str, Mapping[str, Any]]] = None):
        """
        Decorator for the `db_utils` command script entry_point.
        Creates `db_utils_command` wrapper around it.

          Using this method - is the most recommended way to mark command entry point.

        :param command: command name - will be used as command to activate current subcommand
        :param description: command description - will be displayed in current subcommand help
        :param argsetup: command `argparse` subparser setup function (for fast setup - use `args` param instead)
        :param args: options for the command subparser arguments (`argsetup` will be generated automatically)
        """

        # Handle `argsetup` & `args` input
        if argsetup is None:
            # Build `argsetup` based on `args` if `argsetup` is not provided or stub func if `args` not provided also
            argsetup = cls._build_argsetup(args) if args is not None else lambda _: None

        # Return class wrapped into `functools.partial`, picking up all handled arguments
        return partial(cls, command=command, description=description, argsetup=argsetup)

    # ------ Service static methods

    @staticmethod
    def _build_argsetup(args: Iterable[Sequence[Iterable[str], Mapping[str, Any]]]) -> Callable[[ArgumentParser], None]:
        """Builds `argsetup` function using arguments parameters iterable passed by `args`."""

        def argsetup(parser: ArgumentParser):
            """Adds arguments to parser using params passed by `args`."""

            for name_or_flags, options in args:
                if type(name_or_flags) is str:
                    parser.add_argument(name_or_flags, **options)
                else:
                    parser.add_argument(*name_or_flags, **options)

        return argsetup

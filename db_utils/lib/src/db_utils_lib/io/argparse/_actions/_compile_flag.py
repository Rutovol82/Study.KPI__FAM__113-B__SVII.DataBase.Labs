from argparse import Action
from enum import Flag

from functools import reduce


# noinspection PyShadowingBuiltins
class CompileFlag(Action):
    """
    Allows to provide `enum.Flag` input using `argparse`.

      Compiles a resulting flag from string literals corresponds flags names.

        NOTE:

        * This works on the codebase of default `'store'` action
        * `type` for CompileFlag action must be a subclass of `enum.Flag`
        * `const` & `nargs` must NOT be specified
    """

    # ------ Protected fields

    _flag_type: type[Flag]      # Type of target flag (`enum.Flag` subclass)

    # ------ `__init__()` method

    def __init__(self,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):

        # Validate `type`
        # noinspection PyTypeChecker
        if not issubclass(type, Flag):
            raise TypeError("type for FlagCompiler must be a subclass of enum.Flag")

        # Validate `nargs`
        if nargs is not None:
            raise ValueError("nargs is not supported by CompileFLag action; "
                             "it will be defaulted to '+' in any case")

        # Validate `const`
        if const is not None:
            raise ValueError("const is not supported by CompileFLag action")

        # Handle choices
        choices = choices if choices is not None else list(map(lambda _x: _x.name, type))

        # Call superclass `__init__()`
        super().__init__(option_strings=option_strings, dest=dest, metavar=metavar,
                         default=default, required=required, choices=choices, help=help,
                         type=str, nargs='+')

        # Set own attributes
        self._flag_type = type

    # ------ `__call__()` method

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, reduce(lambda _f, _s: _f | self._flag_type[_s.upper()], values, 0))

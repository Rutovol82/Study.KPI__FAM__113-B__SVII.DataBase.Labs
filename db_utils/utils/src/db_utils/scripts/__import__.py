from pathlib import Path
from importlib import import_module

from . import db_utils_command
from . import __name__ as this


# Define public vivible members
__all__ = ['import_commands', 'COMMANDS']


def import_commands() -> dict[db_utils_command]:
    """
    Imports all commands from the current module

    :return: dictionary of imported `db_utils_command` instances
    """

    # Initialize commands dict
    commands = dict()

    # Obtain module path
    module_path = Path(__file__).parent

    # Try to import each `*.py` file, which not starts with '_' from directory
    for script_name in (f.stem for f in module_path.glob('[!_]*.py') if f.is_file()):

        try:
            # Dynamically import possible script module from scripts
            module = import_module('.' + script_name, package=this)

            # Check is it a command script & append to scripts if yes
            if type(module.__command__) is db_utils_command:
                commands[module.__command__.command] = module.__command__

        except (ModuleNotFoundError, AttributeError) as e:
            pass

    return commands


COMMANDS = import_commands()

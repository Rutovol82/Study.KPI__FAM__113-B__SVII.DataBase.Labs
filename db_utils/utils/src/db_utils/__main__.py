from collections.abc import Iterable

import sys
from os import PathLike

from db_utils_lib.db.wrapper import Dumper
from db_utils_lib.std_utils import RetryOpts

from .scripts import COMMANDS, db_utils_command

from db_utils_lib.io.argparse import NamespaceTree
from argparse import ArgumentParser, Namespace

import csv

from db_utils_lib.runtimer import STOPPED, runtimer, timers
from loguru import logger


# ------ Arguments parsing & managing functions

def _setup_logging_params_args(parser: ArgumentParser, base_dest: str = None):
    """
    Setup `db_utils` logging parameters arguments in passed `argparse.ArgumentParser`

    :param parser: parser
    :param base_dest: base destination in namespaces tree (optional)
    """

    # Add new argument group for connection parameters
    group = parser.add_argument_group(title='logging parameters')

    # --- Add arguments for connection parameters

    group.add_argument('--log-quite', '-qL',
                       required=False, action='store_true',
                       dest=NamespaceTree.dest_join(base_dest, 'log_quite'),
                       help='Disables logs output to console.')

    group.add_argument('--log-level', '-lL',
                       required=False, type=str, default='WARNING',
                       choices=['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'],
                       dest=NamespaceTree.dest_join(base_dest, 'log_level'), metavar='LOG_LEVEL',
                       help='Specifies logging log-level as one of the next: '
                            'TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL.')


def _setup_runtiming_params_args(parser: ArgumentParser, base_dest: str = None):
    """
    Setup `db_utils` run time measurement parameters arguments in passed `argparse.ArgumentParser`

    :param parser: parser
    :param base_dest: base destination in namespaces tree (optional)
    """

    # Add new argument group for connection parameters
    group = parser.add_argument_group(title='time measurement parameters')

    # --- Add arguments for connection parameters

    group.add_argument('--timing-file', '-fT',
                       type=str, default=None,
                       dest=NamespaceTree.dest_join(base_dest, 'timing_file'), metavar='TIMING_FILE',
                       help='File path to save global time measurements sample.')


def _setup_conn_params_args(parser: ArgumentParser, base_dest: str = None):
    """
    Setup connection parameters argument group in passed `argparse.ArgumentParser`.

    :param parser: parser
    :param base_dest: base destination in namespaces tree (optional)
    """

    # Add new argument group for connection parameters
    group = parser.add_argument_group(title='database connection parameters')

    # --- Add arguments for connection parameters

    group.add_argument('--host', '--hostname', '-h',
                       required=False, type=str,
                       dest=NamespaceTree.dest_join(base_dest, 'host'), metavar='HOST',
                       help='Specifies the host name of the machine on which the server is running.')

    group.add_argument('--port', '-p',
                       required=False, type=str,
                       dest=NamespaceTree.dest_join(base_dest, 'port'), metavar='PORT',
                       help='Specifies the TCP port or the local Unix-domain socket file extension '
                            'on which the server is listening for connections.')

    group.add_argument('--dbname', '--db', '-d', '-db',
                       required=False, type=str,
                       dest=NamespaceTree.dest_join(base_dest, 'dbname'), metavar='DBNAME',
                       help='Specifies the name of the database to connect to.')

    group.add_argument('--user', '--username', '-U',
                       required=False, type=str,
                       dest=NamespaceTree.dest_join(base_dest, 'user'), metavar='USERNAME',
                       help='User username that will be used to connect to the database.')

    group.add_argument('--password', '--pass', '-P', '-PS',
                       required=False, type=str,
                       dest=NamespaceTree.dest_join(base_dest, 'password'), metavar='PASSWORD',
                       help='User password that will be used to connect to the database.')


def _setup_retry_opts_args(parser: ArgumentParser, base_dest: str = None):
    """
    Setup Dumper wrapper operations retry options argument group in passed `argparse.ArgumentParser`.

    :param parser: parser
    :param base_dest: base destination in namespaces tree (optional)
    """

    # Add new argument group for connection parameters
    group = parser.add_argument_group(title='database operations retry options')

    # --- Add arguments for connection parameters

    group.add_argument('--re-conn-interval', '-iRC',
                       required=False, type=int, default=1,
                       dest=NamespaceTree.dest_join(base_dest, 're_conn_interval'), metavar='RE_CONN_INTERVAL',
                       help='Specifies the interval in seconds between database reconnection attempts '
                            '(1 second by default).')

    group.add_argument('--re-conn-attempts', '-aRC',
                       required=False, type=int, default=None,
                       dest=NamespaceTree.dest_join(base_dest, 're_conn_attempts'), metavar='RE_CONN_ATTEMPTS',
                       help='Specifies the maximum count of database reconnection attempts (unlimited by default).')

    group.add_argument('--re-exec-interval', '-iRE',
                       required=False, type=int, default=1,
                       dest=NamespaceTree.dest_join(base_dest, 're_exec_interval'), metavar='RE_EXEC_INTERVAL',
                       help='Specifies the interval in seconds between database operations execution attempts '
                            '(1 second by default). '
                            'NOTE: database reconnection always provided between execution attempts, '
                            'so database reconnection parameters also affects operations execution.')

    group.add_argument('--re-exec-attempts', '-aRE',
                       required=False, type=int, default=None,
                       dest=NamespaceTree.dest_join(base_dest, 're_exec_attempts'), metavar='RE_EXEC_ATTEMPTS',
                       help='Specifies the maximum count of database operations execution attempts '
                            '(unlimited by default). '
                            'NOTE: database reconnection always provided between execution attempts, '
                            'so database reconnection parameters also affects operations execution.')


def _setup_commands_subparsers(parser: ArgumentParser, commands: Iterable[db_utils_command], dest: str = None):
    """
    Setup subparsers group for commands

    :param parser: parser
    :param commands: `db_utils_command` instances iterable
    """

    # Create subparsers group
    subparsers = parser.add_subparsers(title='available commands', dest=dest)

    # Setup subparser for each command
    for command in commands:
        command_parser = subparsers.add_parser(command.command, help=command.description)
        command.setup_parser(command_parser)


def build_parser(commands: Iterable[db_utils_command], generals_dest: str = None) -> ArgumentParser:
    """
    Builds `db_utils` arguments parser.

    :param commands: `db_utils_command` instances iterable
    :param generals_dest: base nested namespace, where all general arguments (defined at root level) will be placed
    """

    # Create `ArgumentParser` instance
    parser = ArgumentParser(conflict_handler='resolve', fromfile_prefix_chars='@')

    # Setup all arguments groups
    _setup_logging_params_args(parser, base_dest=NamespaceTree.dest_join(generals_dest, 'logging_params'))
    _setup_runtiming_params_args(parser, base_dest=NamespaceTree.dest_join(generals_dest, 'timing_params'))
    _setup_conn_params_args(parser, base_dest=NamespaceTree.dest_join(generals_dest, 'conn_params'))
    _setup_retry_opts_args(parser, base_dest=NamespaceTree.dest_join(generals_dest, 'retry_opts'))
    _setup_commands_subparsers(parser, commands, dest=NamespaceTree.dest_join(generals_dest, 'command'))

    # Return built parser
    return parser


def pop_args(args: Namespace, names: Iterable[str], base_name: str = None) -> Iterable:
    """
    Allows to pop values from `Namespace` instance.

    :param args: arguments `Namespace`
    :param names: names of attributes to pop
    :param base_name: base name in namespaces tree (optional)
    :return:
    """

    for name in map(lambda dest: NamespaceTree.dest_join(base_name, dest), names):
        value = getattr(args, name)
        delattr(args, name)
        yield value


# ------ Program setup functions

STDERR_LOGS_FORMAT = \
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> |  <level>{message}</level>"
"""
Format string for `loguru` logging messages targeted to `stderr`.
"""


def setup_logging(args):
    """Very simple setup of `loguru` logging interface by passed arguments namespace."""

    # Remove any existing handlers
    logger.remove()

    # Add basic `stderr` handler if needed
    if not args.log_quite:
        logger.add(sys.stderr, level=args.log_level, format=STDERR_LOGS_FORMAT)


def init_dumper(conn_params_args, retry_opts_args):
    """Initialize `db_utils_lib.db.wrapper.Dumper` by passed arguments namespaces."""

    return Dumper(
        conn_params_args,
        re_conn_opts=RetryOpts(interval=retry_opts_args.re_conn_interval, attempts=retry_opts_args.re_conn_attempts),
        re_exec_opts=RetryOpts(interval=retry_opts_args.re_exec_interval, attempts=retry_opts_args.re_exec_attempts)
    )


# ------ `main()` function & entry point & additional functionality

def save_timing(path: str | PathLike[str]):
    """Write global timing measurement results to `csv` file by `path`."""

    with open(path, mode='w') as f_:
        writer_ = csv.DictWriter(f_, fieldnames=['name', 'HMS', 'seconds'])
        writer_.writeheader()

        # Dump all `STOPPED` timers data
        for id_, timer_ in timers.filter(STOPPED).items():
            writer_.writerow(dict(name=id_, HMS=timer_.total_time_string(), seconds=timer_.total_time))


def main():
    """Program entry point"""

    # Build cmd arguments parser
    parser = build_parser(COMMANDS.values(), generals_dest='__generals__')

    # Parse & handle arguments
    kwargs = dict(parser.parse_args(namespace=NamespaceTree()).kwargs)
    args = kwargs.pop('__generals__')

    # Setup logging
    setup_logging(args.logging_params)

    # Initialize `db_utils_lib.db.wrapper.Dumper` for all further database operations
    dumper = init_dumper(args.conn_params, args.retry_opts)

    # Call command execution
    with logger.catch(), runtimer(__name__):
        COMMANDS[args.command](dumper, **kwargs)

    # Print global timing
    print("", f"Task finished in {timers[__name__].total_time_string()} ({timers[__name__].total_time:0.3f} s.)",
          sep='\n', end='\n\n')

    # Save timing if necessary
    if args.timing_params.timing_file is not None:
        save_timing(args.timing_params.timing_file)


if __name__ == '__main__':
    main()

from os import PathLike
from pathlib import Path

from itertools import islice

from argparse import ArgumentParser


# ------ ArgumentParser instance preparation

def _get_arg_parser() -> ArgumentParser:
    """Initializes script ArgumentParser for the script"""

    # Initialize parser
    arg_parser_ = ArgumentParser(description="Just a little utility for reducing text files by lines.")

    # Setup reduce options group
    reduce_opts_group_ = arg_parser_.add_argument_group("reduce options")
    reduce_opts_group_.add_argument(
        '-i', '--init', type=int, required=False, dest='init',
        help="Number (from 0) of the first line will be handled (defaults to 0)."
    )
    reduce_opts_group_.add_argument(
        '-k', '--keep', type=int, required=False, dest='keep',
        help="Number of the next kept line relatively to the previous (defaults to 1)"
    )
    reduce_opts_group_.add_argument(
        '-s', '--stop', type=int, required=False, dest='stop',
        help="Number of the last line will be handled (defaults to EOF)."
    )

    # Setup files options group
    files_opts_group_ = arg_parser_.add_argument_group("files options")
    files_opts_group_.add_argument(
        '-Sf', '--source-file', type=str, required=True, dest='source_path', metavar='SOURCE_FILE',
        help="Path to source reducing file."
    )
    files_opts_group_.add_argument(
        '-Se', '--source-encoding', type=str, required=False, dest='source_encoding', metavar='SOURCE_ENCODING',
        help="Source file encoding. Defaults to system default."
    )
    files_opts_group_.add_argument(
        '-Tf', '--target-file', type=str, required=False, dest='target_path', metavar='TARGET_FILE',
        help="Path to a target reduced file. Defaults to '[source-dir]/[source-basename].reduced.[source-suffix]'."
    )
    files_opts_group_.add_argument(
        '-Td', '--target-dir', type=str, required=False, dest='target_dir', metavar='TARGET_DIR',
        help="Alternative to the TARGET_PATH - directory for the output file, "
             "where name will be still '[source-basename].reduced.[source-suffix]'. "
             "NOTE: will not be used if TARGET_FILE specified."
    )
    files_opts_group_.add_argument(
        '-Te', '--target-encoding', type=str, required=False, dest='target_encoding',
        help="Target file encoding. Defaults to source encoding."
    )
    files_opts_group_.add_argument(
        '-Ta', '--target-append', action='store_true', required=False, dest='target_append',
        help="Whether to append target file instead of rewrite."
    )

    # Return prepared `ArgumentParser`
    return arg_parser_


# ------ Functions definition

def reduce_file(source_path: str | PathLike[str],
                target_path: str | PathLike[str] = None,
                target_dir: str | PathLike[str] = None,
                keep: int = 1, init: int = None, stop: int = None,
                source_encoding: str = None,
                target_encoding: str = None,
                target_append: bool = False):
    """
    Reduces `source_path` file by lines, starting from `init` to `stop`, keeps each `keep` line
    and writing them to the `target_path` file.

    :param keep: number of the next kept line relatively to the previous (default 1)
    :param init: count of lines to be skipped between two kept lines (optional)
    :param stop: number of the last line will be handled (optional)
    :param source_path: path to source reducing file
    :param target_path: path to a target reduced file
                       (defaults to '`[source-dir]/[source-basename].reduced.[source-suffix]`')
    :param target_dir: alternate to the `target_path` - directory for the output file
                       (where name will be still '`[source-basename].reduced.[source-suffix]`') -
                       if `target_path` specified - this will be ignored
    :param source_encoding: source file encoding (defaults to system default)
    :param target_encoding: target file encoding (defaults to source encoding)
    :param target_append: whether to append target file instead of rewrite (default `False`)

    :raise IOError: on any problems with files
    """

    # Handle inputs except `target_path`
    source_path = Path(source_path)
    target_mode = 'a' if target_append else 'w'
    target_encoding = target_encoding or source_encoding

    # Handle `target_path` separately
    target_path = Path(target_path) if target_path is not None else None
    target_path = target_path or Path(target_dir or source_path.parent).joinpath(
        f'{source_path.stem}.reduced{source_path.suffix}'
    )

    # Open files & call `reduce()`
    with open(source_path, mode='r', encoding=source_encoding) as source_file, \
         open(target_path, mode=target_mode, encoding=target_encoding) as target_file:

        for line in islice(source_file, init, stop, keep):
            target_file.write(line)


# ------ Entry point

if __name__ == '__main__':

    # Parse arguments & display intro
    args_ = _get_arg_parser().parse_args()
    print(f"Reducing {args_.source_path} started...", end='')

    try:
        reduce_file(**vars(args_))

    except IOError as e:
        print("\tfail.", end='\n\n')
        print("Reducing failed according to unknown error: ", e, sep='\n\n', end='\n\n')

    else:
        print("\tdone", end='\n\n')

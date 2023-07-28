from typing import Callable, Any

from functools import reduce

import psycopg2.extensions

from db_utils_lib.db.data import SessionOpts


# Define public visible members
__all__ = ['with_session', 'commit_after']


def with_session(options: SessionOpts, *ops: Callable[[psycopg2.extensions.connection], Any]):
    """
    Wraps passed callables into special 'composite' wrapper, calls all passed callables one by one
    (according to the original order) inside the `SessionOpts` context, which means all made transactions
    will have modifiers, defined by `options` parameter.

      ****

    Resulting wrapper will have next signature:

    `(psycopg2.connection) -> Any`

    Similar signature expected from all passed callables!

      ****

    Take into account that wrapper will return output **ONLY** from the last callable.

      ****

    **NOTE**: This is **NOT** a decorator. If you need to decorate operational function,
    use `transactional()` decorator instead.

    :param options: session options to be set for operation (through `set_session()` method)
    """

    def composite_wrapper(__conn: psycopg2.extensions.connection):
        with options.inject(__conn):
            return reduce(lambda _, op_: op_(__conn), ops, None)

    return composite_wrapper


def commit_after(*ops: Callable[[psycopg2.extensions.connection], Any]):
    """
    Wraps passed callables into special 'composite' wrapper, calls all passed callables one by one
    (according to the original order) inside the `psycopg2.connection` context, which means all made changes
    will be automatically committed/rolled back on function exit.

      ****

    Resulting wrapper will have next signature:

    `(psycopg2.connection) -> Any`

    Similar signature expected from all passed callables!

      ****

    Take into account that wrapper will return output **ONLY** from the last callable.

      ****

    **NOTE**: This is **NOT** a decorator. If you need to decorate operational function,
    use `use_sess_opts()` decorator instead.
    """

    def composite_wrapper(__conn: psycopg2.extensions.connection):
        with __conn:
            return reduce(lambda _, op_: op_(__conn), ops, None)

    return composite_wrapper

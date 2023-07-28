from functools import wraps
from typing import Callable

from db_utils_lib.std_helpers import decorator_builder, sig_inspect

import psycopg2.extensions

from db_utils_lib.db.data import SessionOpts


# Define public visible members
__all__ = ['use_sess_opts', 'transactional']


@decorator_builder
def _operation_wrapper(conn_src: str = None):
    """
    Helper, allows to automatically build db operations decorators.

      Contains functionality to automatically bind `psycopg2.connection` object
      from arguments passed to target callable.

        This means that connection parameter must match one of two conditions:

        + Be the first positional parameter.
        + Be annotated with `psycopg2.connection` class type.
        + Or have name, passed to wrapper by keyword-only `conn_src` argument.

    Decorated by this decorator functional wrapper must have signature similar to the next:

      `example_operation_wrapper(callable_obj: Callable, conn: psycopg2.connection, /, *args, **kwargs)`

         There:

         + `callable_obj` - will take original operation callable, passed to target decorator
         + `conn` - will take bind `psycopg2.connection` object
         + `args`, `kwargs` - will take args & kwargs, passed to target function

    :param conn_src: name of parameter, contains `psycopg2.connection` object, that will be used in operation
    """

    def external_decorator(wrapper: Callable):

        def wrapper_decorator(callable_obj: Callable):

            nonlocal conn_src

            inspected = sig_inspect(callable_obj)

            if conn_src is None:
                conn_param = inspected.index_param.try_by_type(psycopg2.extensions.connection)
                conn_src = conn_param.name if conn_param is not None else None

            @wraps(callable_obj)
            def wrapper_wrapper(*args, **kwargs):
                conn_ = inspected.get_arg.by_name(conn_src, *args, **kwargs) if conn_src is not None else args[0]
                return wrapper(callable_obj, conn_, *args, **kwargs)

            return wrapper_wrapper

        return wrapper_decorator

    return external_decorator


@decorator_builder
def use_sess_opts(conn_src: str = None, /, *, options: SessionOpts):
    """
    Wrapping passed callable into `SessionOpts.inject` context, which means all made transactions
    will have modifiers, defined by `options` parameter.

      The connection class will be automatically taken from the passed function arguments, or it's default values.
      This means that connection parameter must match one of two conditions:

      + Be the first positional parameter.
      + Be annotated with `psycopg2.connection` class type.
      + Or have name, passed to wrapper by keyword-only `conn_src` argument.

    **NOTE**: This function is **NOT** designed to create wrappers inside repetitive operations.
    If you need such functional, take a look at `with_session()` function.

    :param conn_src: name of parameter, contains `psycopg2.connection` object, that will be used in operation
    :param options: session options to be set for operation (through `set_session()` method)
    """

    @_operation_wrapper(conn_src)
    def operation_wrapper(callable_obj: Callable, conn_: psycopg2.extensions.connection, /, *args, **kwargs):
        with options.inject(conn_):
            return callable_obj(*args, **kwargs)


@decorator_builder
def transactional(conn_src: str = None, /):
    """
    Wrapping passed callable into `psycopg2.connection` context, which means all made changes
    will be automatically committed/rolled back on function exit.

      The connection class will be automatically taken from the passed function arguments, or it's default values.
      This means that connection parameter must match one of two conditions:

      + Be the first positional parameter.
      + Be annotated with `psycopg2.connection` class type.
      + Or have name, passed to wrapper by keyword-only `conn_src` argument.

    **NOTE**: This function is **NOT** designed to create wrappers inside repetitive operations.
    If you need such functional, take a look at `commit_after()` function.

    :param conn_src: name of parameter, contains `psycopg2.connection` object, that will be used in operation
    """

    @_operation_wrapper(conn_src)
    def operation_wrapper(callable_obj: Callable, conn_: psycopg2.extensions.connection, /, *args, **kwargs):
        with conn_:
            return callable_obj(*args, **kwargs)

    return operation_wrapper

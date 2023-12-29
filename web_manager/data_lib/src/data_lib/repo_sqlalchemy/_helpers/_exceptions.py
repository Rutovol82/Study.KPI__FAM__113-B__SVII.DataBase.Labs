from typing import Any
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import ArgumentError as SQLAlchemyArgumentError
from sqlalchemy.exc import DataError as SQLAlchemyDataError, IntegrityError as SQLAlchemyIntegrityError

from sqlalchemy.orm.exc import StaleDataError as SQLAlchemyStaleDataError

from data_lib.repo_abc.exceptions import RepoIntegrityError, RepoInternalError, RepoDataError
from data_lib.repo_abc.exceptions import RepoArgumentError


# Define public visible members
__all__ = ['translate_exceptions']


@contextmanager
def translate_exceptions(__arg: Any = None):
    """
    Special ContextManager for raising unified repository exceptions
    from the SQLAlchemy exceptions occurred inside the enclosing context.
    """

    try:
        # Yield out the passed argument
        yield __arg

    except Exception as err:

        # If the exception is a SQLAlchemyError - reraise the corresponding repository exception
        if isinstance(err, SQLAlchemyError):

            if isinstance(err, SQLAlchemyStaleDataError | SQLAlchemyIntegrityError):
                raise RepoIntegrityError(err) from err

            if isinstance(err, SQLAlchemyArgumentError):
                raise RepoArgumentError(err) from err

            if isinstance(err, SQLAlchemyDataError):
                raise RepoDataError(err) from err

            raise RepoInternalError(err) from err

        # Raise RepoArgumentError for all exceptions not belongs to the SQLAlchemy
        raise RepoArgumentError(err) from err

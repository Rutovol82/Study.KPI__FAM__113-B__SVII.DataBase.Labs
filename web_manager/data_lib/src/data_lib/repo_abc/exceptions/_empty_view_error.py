from . import RepoExceptionOperational


class RepoEmptyViewError(RepoExceptionOperational, ValueError):
    """Raised when data are requested from the empty repository data view."""

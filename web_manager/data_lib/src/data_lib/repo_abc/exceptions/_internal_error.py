from . import RepoExceptionOperational


class RepoInternalError(RepoExceptionOperational, RuntimeError):
    """Indicates repository internal runtime error occurrence."""

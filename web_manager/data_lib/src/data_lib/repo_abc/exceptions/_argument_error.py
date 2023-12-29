from . import RepoExceptionBase


class RepoArgumentError(RepoExceptionBase, TypeError):
    """Raised when an invalid or conflicting function argument is supplied to the repository-related function."""

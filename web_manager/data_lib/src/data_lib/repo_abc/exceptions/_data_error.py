from . import RepoExceptionOperational


class RepoDataError(RepoExceptionOperational, TypeError):
    """Indicates mismatch between types of expected and provided repository-related data."""

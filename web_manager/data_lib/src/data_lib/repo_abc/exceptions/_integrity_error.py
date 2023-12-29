from . import RepoExceptionOperational


class RepoIntegrityError(RepoExceptionOperational):
    """Indicates data integrity violation as a result of ongoing repository operation."""

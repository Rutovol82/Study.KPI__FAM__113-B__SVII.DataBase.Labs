from . import RepoExceptionBase


class RepoExceptionOperational(RepoExceptionBase, RuntimeError):
    """Indicates a runtime error occurrence during execution of repository operaion."""

from . import RepoArgumentError


class RepoUnmappedError(RepoArgumentError, TypeError):
    """Raised when a mapping-related operation invoked for a type or instance not mapped in the repository."""

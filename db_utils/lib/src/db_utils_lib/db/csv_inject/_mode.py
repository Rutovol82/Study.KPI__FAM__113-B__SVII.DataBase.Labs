from enum import IntFlag

from db_utils_lib.std_helpers import FlagGetterMixin


# Define public visible members
__all__ = ['Mode', 'CACHE_DISABLE', 'CACHE_REWRITE', 'CACHE_BLOCKED', 'REPO_NOT_INIT']


class Mode(FlagGetterMixin, IntFlag):
    """Injection flags, used for configuring injection process."""

    CACHE_DISABLE = int('0b00001', 2)
    """Do not use cache. Not reed. Not write. Cache info specifications unnecessary."""

    CACHE_REWRITE = int('0b00010', 2)
    """Rewrite cache for current injection even if there are a valid one."""

    CACHE_BLOCKED = int('0b00100', 2)
    """Do not produce cache for current injection. Using of an existing one allowed."""

    REPO_NOT_INIT = int('0b01000', 2)
    """Do not try to initialize db side injections info repository."""


CACHE_DISABLE = Mode.CACHE_DISABLE
CACHE_REWRITE = Mode.CACHE_REWRITE
CACHE_BLOCKED = Mode.CACHE_BLOCKED
REPO_NOT_INIT = Mode.REPO_NOT_INIT

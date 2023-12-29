from abc import ABCMeta

from . import RepoManagerBase


class RepoManagerStat(RepoManagerBase, metaclass=ABCMeta):
    """
    Data repository manager.

      Provides a high-level interface for statistician querying
      to the repository data using the `RepoStatsAPI` capabilities.
    """

from abc import ABCMeta

from . import RepoManagerObjs, RepoManagerView, RepoManagerStat


class RepoManager(RepoManagerObjs, RepoManagerView, RepoManagerStat, metaclass=ABCMeta):
    """
    Data repository manager.

      Provides a complex data access interface,
      combines dedicated interfaces and compatibilities of the next classes

      * :class:`RepoManagerObjs`
      * :class:`RepoManagerStat`
    """

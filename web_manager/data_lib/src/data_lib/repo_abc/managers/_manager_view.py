from abc import ABCMeta, abstractmethod

from . import RepoManagerBase
from ..views import RepoViewInteractive


class RepoManagerView(RepoManagerBase, metaclass=ABCMeta):
    """
    Data repository manager.

      Provides a high-level interface, allows observing large amounts
      of repository data using the `RepoViewsAPI` capabilities.
    """

    @abstractmethod
    def entity_view(self, __cls: type) -> RepoViewInteractive:
        """
        Returns an interactive view over the `__cls` class entity as a :class:`RepoViewInteractive` instance.
        """

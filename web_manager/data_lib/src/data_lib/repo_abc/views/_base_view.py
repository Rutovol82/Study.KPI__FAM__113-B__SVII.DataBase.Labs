from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic


# Define type vars for generic
_TData = TypeVar('_TData')


class RepoBaseView(Generic[_TData], metaclass=ABCMeta):
    """Base class for all repository data views."""

    # ------ Basic properties

    @property
    @abstractmethod
    def size(self) -> int:
        """
        Current view size.
        """

    # ------ Python service method overrides

    def __len__(self):

        # Return the `size` property value
        return self.size

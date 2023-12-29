from abc import ABCMeta, abstractmethod
from typing import TypeVar

import math

from . import RepoBaseView
from . import RepoMaterializedView, RepoPageView
from .. import RepoArgumentError


# Define type vars for generic
_TData = TypeVar('_TData')


class RepoView(RepoBaseView[_TData], metaclass=ABCMeta):
    """Repository data view."""

    # ------ Materialization methods

    @abstractmethod
    def all(self) -> RepoMaterializedView[_TData]:
        """
        Materializes & returns all data from the current view
        as a :class:`RepoMaterializedView` instance.
        """

    @abstractmethod
    def first(self) -> _TData:
        """
        Materializes & returns first item of the current view.
        """

    # ------ --- Pagination methods

    @property
    @abstractmethod
    def page_size(self) -> int | None:
        """
        Default page size for the current view (`None` if not set).
        """

    def page_count(self, page_size: int = None) -> int:
        """
        Current view pages count for the given `page_size`
        (if not provided - default view page size will be taken).

        :raise RepoArgumentError: if `page_size` is not provided neither by argument, nor by the view default value
        """

        return math.ceil(self.size / self._get_page_size(page_size))

    @abstractmethod
    def page(self, __num: int, /, page_size: int = None) -> RepoPageView[_TData]:
        """
        Materialize & return page number `__num` of the current view for the given `page_size`
        (if not provided - default view page size will be taken).

        :raise RepoArgumentError: if `page_size` is not provided neither by argument, nor by the view default value
        """

    # ------ --- --- Pagination service methods

    def _get_page_size(self, page_size: int = None):
        """
        Service methods, helps to obtain page size from the passed argument or the view default value
        or generate proper exception if any source does not provide page size.

        :return: obtained page size
        :raises RepoArgumentError: if `page_size` is not provided neither by argument, nor by the view default value
        """

        # Handle all possible page size sources
        page_size = page_size or self.page_size

        # Check if value provided
        if page_size is None:
            raise RepoArgumentError(
                "Page size for the view is not provided neither by argument, nor by the view default value."
            )

        # Return obtained value
        return page_size

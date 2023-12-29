from abc import ABCMeta
from typing import TypeVar

from . import RepoBaseView


# Define type vars for generic
_TData = TypeVar('_TData')


class RepoMaterializedView(RepoBaseView[_TData], metaclass=ABCMeta):
    """Repository materialized data view."""



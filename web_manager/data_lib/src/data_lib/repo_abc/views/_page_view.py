from abc import ABCMeta, abstractmethod
from typing import TypeVar

from . import RepoMaterializedView


# Define type vars for generic
_TData = TypeVar('_TData')


class RepoPageView(RepoMaterializedView[_TData], metaclass=ABCMeta):
    pass

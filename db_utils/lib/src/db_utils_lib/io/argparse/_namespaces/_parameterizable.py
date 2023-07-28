from argparse import Namespace
from types import MappingProxyType
from typing import Mapping, Any, Sequence

from db_utils_lib.std_utils import Parameterizable


class ParameterizableNamespace(Parameterizable, Namespace):
    """
    Little modification of original `argparse.Namespace`,
    adds support of `db_utils_lib.std_utils.Parameterizable` interface.
    """

    @property
    def args(self) -> Sequence[Any]:
        return tuple()

    @property
    def kwargs(self) -> Mapping[str, Any]:
        return MappingProxyType(vars(self))

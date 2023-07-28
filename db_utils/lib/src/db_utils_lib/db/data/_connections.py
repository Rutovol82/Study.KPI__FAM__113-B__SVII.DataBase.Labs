from dataclasses import dataclass, asdict
from typing import Mapping, Any, Sequence

from db_utils_lib.std_utils import Parameterizable


@dataclass
class ConnParams(Parameterizable):
    """
    Dataclass to store connection parameters.
    Fields corresponds `psycopg2.connect()` commonn parameters.
    """

    host: str
    port: str

    dbname: str

    user: str
    password: str

    @property
    def args(self) -> Sequence[Any]:
        return tuple()

    @property
    def kwargs(self) -> Mapping[str, Any]:
        return asdict(self)

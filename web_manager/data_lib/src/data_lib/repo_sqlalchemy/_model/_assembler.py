from collections.abc import Callable

from sqlalchemy.orm import registry


class MappingAssembler:
    """Provides assembling application data model SQLAlchemy mapping."""

    # ------ Protected fields

    _units: list[Callable[[registry], None]]

    # ------ Instantiation methods

    def __init__(self):
        """Initializes new instance of `MappingAssembler` class."""

        self._units = list()

    # ------ Functionality methods

    def register_unit(self, __unit: Callable[[registry], None]) -> Callable[[registry], None]:
        """
        Registers new mapping unit.

        Can be used as a decorator (returns passed object).

          ----

        Mapping unit is an object takes care of some unit of mapping process.

        It must be callable with a signature similar to the next:

          `(orm.registry) -> None`
        """

        self._units.append(__unit)

        return __unit

    def assemble_mapping(self, __reg: registry) -> registry:
        """
        Assembles application data model mapping for the given `orm.registry` instance
        using registered mapping units.

        Returns passed registry instance.
        """

        for unit_ in self._units:
            unit_(__reg)

        return __reg

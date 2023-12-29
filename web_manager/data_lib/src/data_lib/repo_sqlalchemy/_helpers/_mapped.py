from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Mapper

from data_lib.repo_abc import RepoArgumentError, RepoUnmappedError


# Define public visible members
__all__ = ['mapped']


# noinspection PyPep8Naming
class mapped:
    """
    Utility methods, provides various helpful operations
    over the objects mapped by the `SQLAlchemy`.
    """

    @staticmethod
    def inspect(__obj: object, /, *, raiseerr: bool = True) -> Mapper | None:
        """
        Returns `SQLAlchemy` ORM :class:`Mapper` for the passed `__obj` object.

          If passed object is not mapped, will raise a :class:`RepoUnmappedError` or return `None`,
          depending on the `raiseerr` value.

        :param __obj: object to obtain :class:`Mapper` for
        :param raiseerr: if `True` - will raise :class:`RepoUnmappedError` if `__obj` is not mapped,
                         otherwise will return `None` (`True` by default)

        :return: :class:`Mapper` object or `None`

        :raise RepoUnmappedError: if `__obj` is not mapped and `raiseerr` is `True`
        """

        # Try to extract mapper from the object
        try:
            # noinspection PyUnresolvedReferences
            return __obj.__mapper__

        # Handle case when the passed object is not mapped
        except AttributeError:

            if not raiseerr:
                return None

            raise RepoUnmappedError(f"Type {type(__obj)} of the passed object is not mapped for the repository.")

    @staticmethod
    def merge(__dst_obj: object, __src_obj: object, /, *, override: bool = False):
        """
        Fill mapped with SQLAlchemy mapping attributes of the `__dst_obj`
        with the values of corresponding attributes from the `__src_obj`.

          Depending on the `override` value will fill only those attributes, which stores `None` values
          (if `override == True`) or all corresponding attributes (otherwise).

        :param __dst_obj: destination object to be filled
        :param __src_obj: source object to take value from
        :param override: whether to override not-`None` attributes of the `__dst_obj`

        :raise RepoUnmappedError: on `__dst_obj` is not mapped
        """

        # Run attributes merge
        try:
            # noinspection PyTypeChecker
            for __name in (__attr.key for __attr in mapped.inspect(type(__dst_obj)).attrs
                           if getattr(__dst_obj, __attr.key) is None):

                setattr(__dst_obj, __name, getattr(__src_obj, __name))

        # Raise a RepoArgumentException if there are differences in attribute sets between merging objects
        except AttributeError as err:
            raise RepoArgumentError("Merging objects expected to have identical attributes set.") from err

    @staticmethod
    def as_dict(__obj: object, /) -> Mapping[str, Any]:
        """
        Obtain a :class:`Mapping` of `SQLAlchemy`-mapped object attributes.

        :param __obj: object to obtain :class:`Mapper` for
        :return: passed object attributes :class:`Mapping`

        :raise RepoUnmappedError: on `__obj` is not mapped
        """

        # noinspection PyTypeChecker
        return {__attr.key: getattr(__obj, __attr.key) for __attr in mapped.inspect(__obj).attrs}

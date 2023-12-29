from typing import Any
from abc import ABCMeta, abstractmethod
from collections.abc import Collection, Sequence, Mapping

from . import RepoManagerBase


class RepoManagerObjs(RepoManagerBase, metaclass=ABCMeta):
    """
    Data repository manager.

      Provides an object-level data access interface,
      includes not much more as a basic CRUD capabilities.
    """

    # ------ Attribute-taking methods

    # ------ --- Create methods

    @abstractmethod
    def insert(self, __cls: type, __vals_map: Mapping[str, Any] = None, /, **__vals: Any) -> object:
        """
        Insert new instance of the `__cls` class into the repository using the passed attribute values.

        :param __cls: entity class
        :param __vals_map: attribute name to value :class:`Mapping` (if not provided - `__vals` will be taken)
        :param __vals: attribute values (if `__vals_map` provided - will be ignored)

        :return: inserted object
        """

    def insert_all(self, __cls: type, __vals_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object]:
        """
        Insert new instances of the `__cls` class into the repository using the passed attribute values.

        :param __cls: entity class
        :param __vals_maps: :class:`Sequence` of attribute name to value :class:`Mapping` objects for each new instance

        :return: :class:`Sequence` of inserted objects
        """

        # Default implementation just calls `insert()` for each instance
        return [self.insert(__cls, __vals_map) for __vals_map in __vals_maps]

    # ------ --- Read methods

    @abstractmethod
    def exists(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> bool:
        """
        Check for the existence of the `__cls` instance with the passed key attributes in the repository.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_map: key attribute name to value :class:`Mapping` (if not provided - `__keys` will be taken)
        :param __keys: key attribute values (if `__keys_map` provided - will be ignored)

        :return: `True` if instance exists in the repository, `False` otherwise
        """

    @abstractmethod
    def select(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> object | None:
        """
        Select instance of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_map: key attribute name to value :class:`Mapping` (if not provided - `__keys` will be taken)
        :param __keys: key attribute values (if `__keys_map` provided - will be ignored)

        :return: selected object or `None` value (if requested instance did not exist)
        """

    def exists_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[bool]:
        """
        Check for the existence of the `__cls` instances with the passed key attributes in the repository.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_maps: :class:`Sequence` of key attribute name to value :class:`Mapping` objects for each instance

        :return: :class:`Sequence` of :class:`bool` values,
                 indicates whether the corresponding instance exists in the repository
        """

        # Default implementation just calls `exists()` for each instance
        return [self.exists(__cls, __keys_map) for __keys_map in __keys_maps]

    def select_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object | None]:
        """
        Select instances of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_maps: :class:`Sequence` of key attribute name to value :class:`Mapping` objects for each instance

        :return: :class:`Sequence` of selected objects or `None` values (if requested instances did not exist)
        """

        # Default implementation just calls `select()` for each instance
        return [self.select(__cls, __keys_map) for __keys_map in __keys_maps]

    def exists_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> bool:
        """
        Check for the existence of any `__cls` instances with attributes matches to the passed values in the repository.

        :param __cls: entity class
        :param __attr_map: attribute name to value :class:`Mapping`

        :return: `True` if at least one instance exists in the repository, otherwise `False`
        """

        # Raise :class:`NotImplementedError` as a default implementation
        raise NotImplementedError()

    def select_any(self, __cls: type, __attr_map: Mapping[str, Any], /, *, limit: int = None) -> Collection[object]:
        """
        Select instances of the `__cls` class from the repository with attributes matches to the passed values.

        :param __cls: entity class
        :param __attr_map: attribute name to value :class:`Mapping`
        :param limit: maximum number of selected objects

        :return: :class:`Collection` of selected objects
        """

        # Raise :class:`NotImplementedError` as a default implementation
        raise NotImplementedError()

    # ------ --- Update methods

    @abstractmethod
    def update(self, __cls: type, __keys_vals_map: Mapping[str, Any] = None, /, **__keys_vals: Any):
        """
        Update instance of the `__cls` class stored in the repository with the passed attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_vals_map: attribute name to value :class:`Mapping` (if not provided - `__keys_vals` will be taken)
        :param __keys_vals: attribute values (if `__keys_vals_map` provided - will be ignored)
        """

    def update_all(self, __cls: type, __keys_vals_maps: Sequence[Mapping[str, Any]], /):
        """
        Update instances of the `__cls` class stored in the repository with the passed attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_vals_maps: :class:`Sequence` of attribute name to value :class:`Mapping` objects for each instance
        """

        # Default implementation just calls `update()` for each instance
        for __keys_vals_map in __keys_vals_maps:
            self.update(__cls, __keys_vals_map)

    # ------ --- Delete methods

    @abstractmethod
    def delete(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> bool:
        """
        Delete instance of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_map: key attribute name to value :class:`Mapping` (if not provided - `__keys` will be taken)
        :param __keys: key attribute values (if `__keys_map` provided - will be ignored)

        :return: `True` if the object was successfully deleted from the repository, `False` otherwise
        """

    @abstractmethod
    def popout(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> object | None:
        """
        Delete & return instance of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_map: key attribute name to value :class:`Mapping` (if not provided - `__keys` will be taken)
        :param __keys: key attribute values (if `__keys_map` provided - will be ignored)

        :return: selected object or `None` value (if requested instance did not exist)
        """

    def delete_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[bool]:
        """
        Delete instances of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_maps: :class:`Sequence` of key attribute name to value :class:`Mapping` objects for each instance

        :return: :class:`Sequence` of :class:`bool` values,
                 indicates whether the corresponding instance was successfully deleted from the repository
        """

        # Default implementation just calls `delete()` for each instance
        return [self.delete(__cls, __keys_map) for __keys_map in __keys_maps]

    def popout_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object | None]:
        """
        Delete & return instances of the `__cls` class from the repository by the passed key attribute values.

          **NOTE:** Passed attributes must specify values for all the identity attributes.

        :param __cls: entity class
        :param __keys_maps: :class:`Sequence` of key attribute name to value :class:`Mapping` objects for each instance

        :return: :class:`Sequence` of deleted objects or `None` values (if requested instances did not exist)
        """

        # Default implementation just calls `popout()` for each instance
        return [self.popout(__cls, __keys_map) for __keys_map in __keys_maps]

    @abstractmethod
    def delete_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> int:
        """
        Delete instances of the `__cls` class from the repository with attributes matches to the passed values.

        :param __cls: entity class
        :param __attr_map: attribute name to value :class:`Mapping`

        :return: number of deleted objects
        """

        # Raise :class:`NotImplementedError` as a default implementation
        raise NotImplementedError()

    @abstractmethod
    def popout_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> Collection[object]:
        """
        Delete & return instances of the `__cls` class from the repository with attributes matches to the passed values.

        :param __cls: entity class
        :param __attr_map: attribute name to value :class:`Mapping`

        :return: :class:`Collection` of deleted objects
        """

        # Raise :class:`NotImplementedError` as a default implementation
        raise NotImplementedError()

    # ------ Object-taking methods

    # ------ --- Create methods

    @abstractmethod
    def append(self, __obj: object, /, *, inplace: bool = True, override: bool = False) -> object:
        """
        Append the passed object to the repository.

          Depending on the `inplace` value, will return new object,
          identical to passed, but with filled auto-generated attribute values (if `inplace == True`),
          or will fill those values directly into the passed object (otherwise).

            In case of filling the passed object, there are two options, depending on the `override`:
            override all attributes with corresponding values from the repository (`override == True`)
            or fill only those, which are `None` (otherwise).

        :param __obj: object to be appended
        :param inplace: whether to return a new instance or modify the passed one (`True` by default)
        :param override: if modifying the passed object, whether to override not-`None` attributes (`False` by default)

        :return: appended object as new instance from the repository or modified passed object,
                 depending on the `inplace` value
        """

    def append_all(self, __objs: Sequence[object], /, *, inplace: bool = True, override: bool = False) -> Sequence[object]:
        """
        Append the passed objects to the repository.

          Depending on the `inplace` value, will return a :class:`Sequence` of new objects,
          identical to passed, but with filled auto-generated attribute values (if `inplace == True`),
          or will fill those values directly into the passed objects (otherwise).

            In case of filling the passed objects, there are two options, depending on the `override`:
            override all attributes with corresponding values from the repository (`override == True`)
            or fill only those, which are `None` (otherwise).

        :param __objs: :class:`Sequence` of objects to be appended
        :param inplace: whether to return a new instances or modify the passed ones (`True` by default)
        :param override: if modifying the passed objects, whether to override not-`None` attributes (`False` by default)

        :return: :class:`Sequence` of appended objects as new instances from the repository or modified passed objects,
                 depending on the `inplace` value
        """

        # Default implementation just calls `insert()` for each object
        return [self.append(__obj, inplace=inplace, override=override) for __obj in __objs]

    # ------ --- Read methods

    @abstractmethod
    def stores(self, __obj: object, /) -> bool:
        """
        Check for the existence of the passed object in the repository.

          **NOTE:** Passed object must contain values for all the identity attributes.

        :param __obj: object to be checked

        :return: `True` if object is stored in the repository, `False` otherwise
        """

    def __contains__(self, __obj):

        # Pass call to the `stores()` method
        return self.stores(__obj)

    @abstractmethod
    def fillup(self, __obj: object, /, *, inplace: bool = True, override: bool = False) -> object:
        """
        Fill up attributes of the passed object with the values from the repository.

          **NOTE:** Passed object must contain values for all the identity attributes.

            Depending on the `inplace` value, will create new object to be modified (if `inplace == True`),
            or will fill the passed object directly (otherwise).

              In case of filling the passed object, there are two options, depending on the `override`:
              override all attributes with corresponding values from the repository (`override == True`)
              or fill only those, which are `None` (otherwise).

        :param __obj: object to be filled
        :param inplace: whether to return a copy or modify the passed object (`True` by default)
        :param override: if modifying the passed object, whether to override not-`None` attributes (`False` by default)

        :return: filled passed object or it's copy, depending on the `inplace` value
        """

    def stores_all(self, __objs: Sequence[object], /) -> Sequence[bool]:
        """
        Check for the existence of the passed objects in the repository.

          **NOTE:** Passed objects must contain values for all the identity attributes.

        :param __objs: :class:`Sequence` of objects to be checked

        :return: :class:`Sequence` of :class:`bool` values,
                 indicates whether the corresponding object is stored in the repository
        """

        # Default implementation just calls `stores()` for each object
        return [self.stores(__obj) for __obj in __objs]

    def fillup_all(self, __objs: Sequence[object], /, *, inplace: bool = True, override: bool = False) -> Sequence[object]:
        """
        Fill up attributes of the passed objects with the values from the repository.

          **NOTE:** Passed objects must contain values for all the identity attributes.

            Depending on the `inplace` value, will create new objects to be modified (if `inplace == True`),
            or will fill the passed objects directly (otherwise).

              In case of filling the passed objects, there are two options, depending on the `override`:
              override all attributes with corresponding values from the repository (`override == True`)
              or fill only those, which are `None` (otherwise).

        :param __objs: objects to be filled
        :param inplace: whether to return a copies or modify the passed objects (`True` by default)
        :param override: if modifying the passed objects, whether to override not-`None` attributes (`False` by default)

        :return: :class:`Sequence` of filled passed objects or their copies, depending on the `inplace` value
        """

        # Default implementation just calls `fillup()` for each object
        return [self.fillup(__obj, inplace=inplace, override=override) for __obj in __objs]

    # ------ --- Update methods

    @abstractmethod
    def modify(self, __obj: object, /) -> object:
        """
        Modify object stored in the repository with its new version presented by passed object.

          **NOTE:** Passed object must contain values for all the identity attributes.

        :param __obj: target object

        :return: passed object (without any changes)
        """

    def modify_all(self, __objs: Sequence[object], /) -> Sequence[object]:
        """
        Modify objects stored in the repository with their new versions presented by passed objects.

          **NOTE:** Passed objects must contain values for all the identity attributes.

        :param __objs: :class:`Sequence` of target objects

        :return: passed objects :class:`Sequence` (without any changes)
        """

        # Default implementation just calls `modify()` for each object
        for __obj in __objs:
            self.modify(__obj)

        return __objs

    # ------ --- Delete methods

    @abstractmethod
    def remove(self, __obj: object, /) -> bool:
        """
        Remove the passed object from the repository.

          **NOTE:** Passed object must contain values for all the identity attributes.

        :param __obj: object to be removed

        :return: `True` if the object was successfully removed from the repository, `False` otherwise
        """

    def remove_all(self, __objs: Sequence[object], /) -> Sequence[bool]:
        """
        Remove the passed objects from the repository.

          **NOTE:** Passed objects must contain values for all the identity attributes.

        :param __objs: :class:`Seuqence` of objects to be removed

        :return: :class:`Sequence` of :class:`bool` values,
                 indicates whether the corresponding object was successfully removed from the repository
        """

        # Default implementation just calls `remove()` for each object
        return [self.remove(__obj) for __obj in __objs]

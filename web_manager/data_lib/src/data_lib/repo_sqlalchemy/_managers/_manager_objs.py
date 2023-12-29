from collections.abc import Collection, Sequence, Mapping
from typing import Any

from sqlalchemy import insert, select, update, delete

from data_lib.repo_abc import RepoManagerObjs
from . import SQLAlchemyRepoManagerBase

from .._helpers import translate_exceptions, mapped


class SQLAlchemyRepoManagerObjs(SQLAlchemyRepoManagerBase, RepoManagerObjs):
    """`SQLAlchemy` data repository :class:`RepoManagerObjs` manager."""

    # ------ Attribute-taking methods

    # ------ --- Create methods

    def insert(self, __cls: type, __vals_map: Mapping[str, Any] = None, /, **__vals: Any) -> object:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute insertion
                return self._session.execute(insert(__cls).returning(__cls), [__vals_map or __vals]).scalar_one()

    def insert_all(self, __cls: type, __vals_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute insertions
                return self._session.execute(insert(__cls).returning(__cls), __vals_maps).scalars().all()

    # ------ --- Read methods

    def exists(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> bool:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selection
                return self._session.execute(
                    select(select(__cls).filter_by(**(__keys_map or __keys)).exists())
                ).scalar_one()

    def select(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> object | None:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selection
                return self._session.execute(
                    select(__cls).filter_by(**(__keys_map or __keys)).limit(1)
                ).scalar_one_or_none()

    def exists_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[bool]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selections
                return [
                    self._session.execute(select(select(__cls).filter_by(**__keys_map).exists())).scalar_one()
                    for __keys_map in __keys_maps
                ]

    def select_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object | None]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selections
                return [
                    self._session.execute(select(__cls).filter_by(**__keys_map).limit(1)).scalar_one_or_none()
                    for __keys_map in __keys_maps
                ]

    def exists_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> bool:

        # Pass call to the `exists()` method
        return self.exists(__cls, __attr_map)

    def select_any(self, __cls: type, __attr_map: Mapping[str, Any], /, *, limit: int = None) -> Collection[object]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selection
                return self._session.execute(select(__cls).filter_by(**__attr_map).limit(limit)).scalars().all()

    # ------ --- Update methods

    def update(self, __cls: type, __keys_vals_map: Mapping[str, Any] = None, /, **__keys_vals: Any):

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute update
                self._session.execute(update(__cls), [__keys_vals_map or __keys_vals])

    def update_all(self, __cls: type, __keys_vals_maps: Sequence[Mapping[str, Any]], /):

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute updates
                self._session.execute(update(__cls), __keys_vals_maps)

    # ------ --- Delete methods

    def delete(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> bool:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute deletion
                return bool(self._session.execute(
                    delete(__cls).filter_by(**(__keys_map or __keys))
                ).rowcount)

    def popout(self, __cls: type, __keys_map: Mapping[str, Any] = None, /, **__keys: Any) -> object | None:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selection
                return self._session.execute(
                    delete(__cls).filter_by(**(__keys_map or __keys)).returning(__cls)
                ).scalar_one_or_none()

    def delete_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[bool]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute deletion
                return [
                    bool(self._session.execute(delete(__cls).filter_by(**__keys_map)).rowcount)
                    for __keys_map in __keys_maps
                ]

    def popout_all(self, __cls: type, __keys_maps: Sequence[Mapping[str, Any]], /) -> Sequence[object | None]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute deletion
                return [
                    self._session.execute(delete(__cls).filter_by(**__keys_map).returning(__cls)).scalar_one_or_none()
                    for __keys_map in __keys_maps
                ]

    def delete_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> int:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute deletion
                return self._session.execute(
                    delete(__cls).filter_by(**__attr_map)
                ).rowcount

    def popout_any(self, __cls: type, __attr_map: Mapping[str, Any], /) -> Collection[object]:

        # Open exceptions translation & session transaction contexts
        with translate_exceptions():
            with self._session.begin():

                # Execute selection
                return self._session.execute(
                    delete(__cls).filter_by(**__attr_map).returning(__cls)
                ).scalars().all()

    # ------ Object-taking methods

    # ------ --- Create methods

    def append(self, __obj: object, /, *, inplace: bool = True, override: bool = False) -> object:

        # Insert instance into the repository using the `insert()` method
        __new_obj = self.insert(type(__obj), mapped.as_dict(__obj))

        # Dispatch behavior and return inserted object
        return mapped.merge(__obj, __new_obj, override=override) if inplace else __new_obj

    def append_all(self, __objs: Sequence[object], /, *, inplace: bool = True, override: bool = False) -> Sequence[object]:

        # Check if the `__objs` sequence is empty
        if len(__objs) == 0:
            return []

        # Insert instances into the repository using the `insert_all()` method
        __new_objs = self.insert_all(type(__objs[0]), list(map(mapped.as_dict, __objs)))

        # Dispatch behavior and return inserted objects sequence
        return [mapped.merge(__obj, __new_obj, override=override) for __obj, __new_obj in zip(__objs, __new_objs)]  \
            if inplace else __new_objs

    # ------ --- Read methods

    def stores(self, __obj: object, /) -> bool:

        # Pass call to the `exists()` method
        return self.exists(type(__obj), mapped.as_dict(__obj))

    def fillup(self, __obj: object, /, *, inplace: bool = True, override: bool = False) -> object:

        # Select instance from the repository using the `select()` method
        __new_obj = self.select(type(__obj), mapped.as_dict(__obj))

        # Dispatch behavior and return inserted object
        return mapped.merge(__obj, __new_obj, override=override) if inplace else __new_obj

    def stores_all(self, __objs: Sequence[object], /) -> Sequence[bool]:

        # Check if the `__objs` sequence is empty
        if len(__objs) == 0:
            return []

        # Pass call to the `exists_all()` method
        return self.exists_all(type(__objs[0]), list(map(mapped.as_dict, __objs)))

    def fillup_all(self, __objs: Sequence[object], /, *, inplace: bool = True, override: bool = False) -> Sequence[object]:

        # Check if the `__objs` sequence is empty
        if len(__objs) == 0:
            return []

        # Select instances from the repository using the `select_all()` method
        __new_objs = self.select_all(type(__objs[0]), list(map(mapped.as_dict, __objs)))

        # Dispatch behavior and return inserted objects sequence
        return [mapped.merge(__obj, __new_obj, override=override) for __obj, __new_obj in zip(__objs, __new_objs)] \
            if inplace else __new_objs

    # ------ --- Update methods

    def modify(self, __obj: object, /) -> object:

        # Updated instance in the repository using the `update()` method
        self.update(type(__obj), mapped.as_dict(__obj))

        # Return passed object without any changes
        return __obj

    def modify_all(self, __objs: Sequence[object], /) -> Sequence[object]:

        # Check if the `__objs` sequence is empty
        if len(__objs) != 0:
            # Updated instances in the repository using the `update_all()` method
            self.update_all(type(__objs[0]), list(map(mapped.as_dict, __objs)))

        # Return passed objects sequence without any changes
        return __objs

    # ------ --- Delete methods

    def remove(self, __obj: object, /) -> bool:

        # Pass call to the `delete()` method
        return self.delete(type(__obj), mapped.as_dict(__obj))

    def remove_all(self, __objs: Sequence[object], /) -> Sequence[bool]:

        # Check if the `__objs` sequence is empty
        if len(__objs) == 0:
            return []

        # Pass call to the `delete_all()` method
        return self.delete_all(type(__objs[0]), list(map(mapped.as_dict, __objs)))

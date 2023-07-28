from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import Literal, Any

from .... import Config
from ... import Status


class RepositoryContentManagerABC(metaclass=ABCMeta):
    """
    High-level interface for maximally comfortable db-side injections data repository content management.

      ----

    **NOTE**: This interface has limited compatibility with `MutableMapping`. It defines many methods
    with same signatures and similar outputs.

      However, it does not conform to some contracts required by `MutableMapping`
      because of its implementation would unnecessarily affect performance and code complexity.

        So, most likely, you will be able to use `RepositoryContentManagerABC`-derived classes instances as
        in the places where `Mapping`/`MutableMapping` expected, **BUT** only in simple cases, requires only
        basic `MutableMapping` functionality.

          We recommend to pass it as `Mapping`/`MutableMapping` replacement only to code managed by yourself.

            Alternatively, you can get 'in-moment' copy of repository as Python `dict` using `asdict()` method.
    """

    # ------ `Status` instances storage general management methods

    @abstractmethod
    def status_count(self) -> int:
        """Counts stored `Status` instances number."""

    @abstractmethod
    def status_items(self) -> Iterator[tuple[str, Status]]:
        """Returns iterator over tuples of injection id and `Status` instance for all stored records."""

    @abstractmethod
    def status_keys(self) -> Iterator[str]:
        """Returns iterator over injection id's for all stored records."""

    @abstractmethod
    def status_objs(self) -> Iterator[Status]:
        """Returns iterator over `Status` instances for all stored records."""

    # ------ `Status` instances storage CRUD management methods

    @abstractmethod
    def status_select(self, __id: str | Config, *,
                      on_not_exist: Literal['default', 'insert', 'except'] = 'except',
                      default: Any | Status = None) -> Status | None:
        """
        Selects `Status` by id extracted from id string or injection `Config` instance.

          ----

        `on_not_exist` parameter can be used to define behavior on case when `Status`
        with given id not found in the repository. It can take next values:

        * '`default`' - if not exists do nothing & return `default` value
        * '`insert`' - if not exists insert `default` instance & return it
        * '`except`' - if not exists raise KeyError (default)

          ----

        :param __id: injection id string or `Config` instance
        :param on_not_exist: literal defines what to do if `Status` with given id not exists
        :param default: default value - may be returned (& inserted) if given id not found -
                        depends on `on_not_exist` mode

        :raise TypeError: if `default` is not `Status` instance, but `on_not_exist` set to '`insert`'
        :raise KeyError: if `Status` with given id not found and `on_not_exist` set to `except`
        :return: `Status` instance for given injection id or `default` if not found
                 and `on_not_exist` set to '`default`'
        """

    @abstractmethod
    def status_delete(self, __id: str | Config, *,
                      on_not_exist: Literal['default', 'insert', 'except'] = 'except',
                      default: Any | Status = None) -> Status | None:
        """
        Deletes `Status` by id extracted from id string or injection `Config` instance.
        Returns deleted `Status` instance.

          ----

        `on_not_exist` parameter can be used to define behavior on case when `Status`
        with given id not found in the repository. It can take next values:

        * '`default`' - if not exists do nothing & return `default` value
        * '`except`' - if not exists raise KeyError (default)

          ----

        :param __id: injection id string or `Config` instance
        :param on_not_exist: literal defines what to do if `Status` with given id not exists
        :param default: default value - may be returned (& inserted) if given id not found -
                        depends on `on_not_exist` mode

        :raise KeyError: if `Status` with given id not found and `on_not_exist` set to `except`
        :return: deleted `Status` instance for given injection id or `default` if not found
                 and `on_not_exist` set to '`default`'
        """

    @abstractmethod
    def status_insert(self, __id: str | Config, status_: Status, *,
                      on_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
        """
        Places new `Status` by id extracted from id string or injection `Config` instance.

          ----

        `on_exist` parameter can be used to define behavior on case when `Status`
        with given id already exists. It can take next values:

        * '`ignore`' - on conflict do nothing & return `False`, otherwise return `True`
        * '`update`' - on conflict update existing instance, return `True` in both cases
        * '`except`' - on conflict raise KeyError, otherwise return `True`

          ----

        :param __id: injection id string or `Config` instance
        :param status_: injection id string or `Config` instance
        :param on_exist: literal defines what to do if `Status` with given id already exists

        :raise KeyError: if `Status` with given id not found and `on_exist` is `except`
        :raise ValueError: if unknown `on_exist` value passed

        :return: `True` on success, `False` otherwise (NOTE: 'success' depends on `on_exist` mode)
        """

    @abstractmethod
    def status_update(self, __id: str | Config, status_: Status, *,
                      on_not_exist: Literal['ignore', 'update', 'except'] = 'except') -> bool:
        """
        Updates existing `Status` by id extracted from id string or injection `Config` instance.

          ----

        `on_not_exist` parameter can be used to define behavior on case when `Status`
        with given id not found. It can take next values:

        * '`ignore`' - if not exists do nothing & return `False`, otherwise return `True`
        * '`insert`' - if not exists insert new instance, return `True` in both cases
        * '`except`' - if not exists raise KeyError, otherwise return `True`

          ----

        :param __id: injection id string or `Config` instance
        :param status_: `Status` instance to update by
        :param on_not_exist: literal defines what to do if `Status` with given id already exists

        :raise KeyError: if `Status` with given id not found and `on_not_exist` is `except`
        :raise ValueError: if unknown `on_not_exist` value passed

        :return: `True` on success, `False` otherwise (NOTE: 'success' depends on `on_not_exist` mode)
        """

    # ------ `Status` instances storage simplified additional management methods (common actions)

    @abstractmethod
    def status_increment(self, __id: str | Config, *, must_exist: bool = True) -> Status | None:
        """
        Increments `injected` count of already injected blocks in record by id extracted from id string
        or injection `Config` instance. Returns updated `Status` instance.

          ----

        `must_exist` parameter can be used to define behavior on case when `Status` with given id not found.

        * If `must_exist is True` -`KeyError` will be thrown if requested instance not found.
        * If `must_exist is False` - `None` will be returned if requested instance not found.

          ----

        :param __id: injection id string or `Config` instance
        :param must_exist: whether to raise exception if `Status` with given id not found (`True` by default)

        :raise KeyError: if `Status` with given id not found and `must_exist` is `True`

        :return: updated `Status` instance for given injection id or `None` if not found and `must_exist` is `False`
        """

    # ------ `Status` instances storage simplified mapping-alike management methods

    def __len__(self) -> int:
        return self.status_count()

    def count(self):
        """
        Returns count of stored `Status` instances.

          Alias of `__len__()` or `status_count()`
        """

        return self.status_count()

    def __iter__(self) -> Iterator[str]:
        return self.status_keys()

    def items(self) -> Iterator[tuple[str, Status]]:
        """
        Returns iterator over tuples of injection id and `Status` instance for all stored records.

          Mapping-alike alias of `status_items()`
        """
        return self.status_items()

    def keys(self) -> Iterator[str]:
        """
        Returns iterator over injection id's for all stored records.

          Mapping-alike alias of `status_keys()`
        """

        return self.status_keys()

    def values(self) -> Iterator[Status]:
        """
        Returns iterator over `Status` instances for all stored records.

          Mapping-alike alias of `status_objs()`
        """

        return self.status_objs()

    def asdict(self) -> dict[str, Status]:
        """Returns `in-moment` copy of repository content as Python dictionary."""

        return dict(self.status_items())

    def __setitem__(self, __id: str | Config, status_: Status):
        self.status_insert(__id, status_, on_exist='update')

    def set(self, __id: str | Config, status_: Status):
        """
        Places `status_` injection `Status` instance as associated with injection id
        extracted from id string or `Config` instance passed by `__id`.

        :param __id: injection id string or `Config` instance
        :param status_: injection id string or `Config` instance
        """

        self.status_insert(__id, status_, on_exist='update')

    def __getitem__(self, __id: str | Config) -> Status:
        return self.status_select(__id, on_not_exist='except')

    def get(self, __id: str | Config, default: Any = None) -> Status | Any:
        """
        Selects `status_` injection `Status` instance by injection id
        extracted from id string or `Config` instance passed by `__id`.

          If id not found returns `default` value.

        :param __id: injection id string or `Config` instance
        :param default: value to return if specified id not found (`None` by default)
        """

        return self.status_select(__id, on_not_exist='default', default=default)

    def __delitem__(self, __id: str | Config):
        self.status_delete(__id, on_not_exist='except')

    def pop(self, __id: str | Config, *default: Any) -> Status | Any:
        """
        Deletes `status_` injection `Status` instance by injection id
        extracted from id string or `Config` instance passed by `__id`
        and returns deleted instance.

          If id not found returns `default` value if specified, else raises `KeyError`.

        :param __id: injection id string or `Config` instance
        :param default: value to return if specified id not found (`None` by default)

        :raise KeyError: if specified injection id not found and no default value provided.
        """

        # Handle the case when default not passed
        if len(default) == 0:
            return self.status_delete(__id, on_not_exist='except')

        # Handle the case when default passed
        elif len(default) == 1:
            return self.status_delete(__id, on_not_exist='default', default=default)

        # Raise `TypeError` on unsupported arguments set
        raise TypeError(f'{self.pop.__name__}() takes 3 positional arguments but {len(default) + 2} were given')

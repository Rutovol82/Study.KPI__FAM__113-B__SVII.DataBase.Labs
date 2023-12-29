from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager


class RepoManagerBase(AbstractContextManager, metaclass=ABCMeta):
    """
    Data repository manager abstraction.

      ----

    By design, it must be instantiated separately for each task or thread.

      Supports `ContextManager` pattern.
    """

    # ------ `prepare()/release()` methods

    @abstractmethod
    def prepare(self) -> 'RepoManagerBase':
        """
        Prepares the current manager to work with the data repository.

          **NOTE:** Must be invoked before any other action will be done.

          Alternatively: use class as a `ContextManager`.

        :return: self
        """

    @abstractmethod
    def release(self):
        """
        Releases ane resources allocated by the current manager.

          **NOTE:** Must be invoked after the end of manager use.

          Alternatively: use class as a `ContextManager`.
        """

    # ------ `ContextManager` protocol methods

    def __enter__(self):

        # Default implementation just calls `prepare()` method.
        return self.prepare()

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Default implementation just calls `release()` method.
        self.release()

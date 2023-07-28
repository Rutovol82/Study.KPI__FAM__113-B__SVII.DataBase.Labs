# Define public visible members
__all__ = ['SingletonMeta', 'Singleton']


class SingletonMeta(type):
    """
    Singleton metaclass. Use it to easily create singletons.

      **NOTE**: On target classes, the singleton instance, if already exists,
      will be stored in `__instance__` attribute.
    """

    def __call__(cls, *args, **kwargs):

        if not hasattr(cls, '__instance__'):
            setattr(cls, '__instance__', super(cls.__class__, cls).__call__(*args, **kwargs))

        return getattr(cls, '__instance__')


class Singleton:
    """
    Singleton base class. Use it to easily create singletons.

      **NOTE**: On derived classes, the singleton instance, if already exists,
      will be stored in `__instance__` attribute.
    """

    def __new__(cls):

        if not hasattr(cls, '__instance__'):
            setattr(cls, '__instance__', object.__new__(cls))

        return getattr(cls, '__instance__')

from . import ParameterizableNamespace


class NamespaceTree(ParameterizableNamespace):
    """
    Little modification of original `argparse.Namespace`, allows to create nested namespaces.

      It's just overrides `__getattr__` & `__setattr__` methods,
      makes them support '.' delimiter as nesting mark.

        As a part of `db_utils_lib` it is also derived from `ParameterizableNamespace`
        to provide `db_utils_lib.std_utils.Parameterizable` interface support.
    """

    def __setattr__(self, __name, __value):
        names = __name.split('.', 1)
        if len(names) == 1:
            super().__setattr__(__name, __value)

        else:
            nested = self.__dict__.get(names[0], None)
            if nested is None:
                nested = NamespaceTree()
                super().__setattr__(names[0], nested)

            setattr(nested, names[1], __value)

    def __getattr__(self, __name):
        names = __name.split('.', 2)
        superval = getattr(super(), names[0])
        return superval if len(names) == 1 else getattr(superval, names[1])

    @staticmethod
    def dest_join(base: str | None, current: str | None) -> str:
        """
        Helps to join `base` & `current` `argparse` `dest` string,
        handling cases when None passed instead of values.
        """

        return current if base is None else base if current is None else base + '.' + current

# Define public visible members
__all__ = ['extends']


def extends(obj: object, name: str = None):
    """
    Decorator, helps to extend existing objects with new attribute (methods, by design).

      Uses simple `setattr()` approach to add new attribute with specified name
      (if not specified - will take `__name__` from a decorated object if it exists, else raises `TypeError`)
      and value of a decorated object to a specified object.

    :raise TypeError: If `name` not provided & can not be extracted from a decorated object
    :param obj: to be extended
    :param name: new object attribute name
    """

    def decorator(extension_obj: object):

        nonlocal name

        # Try to obtain name if not provided
        if name is None:
            if hasattr(extension_obj, '__name__'):
                name = extension_obj.__name__
            else:
                raise TypeError("Extension name is not specified and can't be extracted from object.")

        # Set new attribute to obj
        setattr(obj, name or extension_obj.__name__, extension_obj)

        # Return decorated object without any changes
        return extension_obj

    # Return decorator
    return decorator

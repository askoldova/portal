import os


def check_exist_and_type(value, name, _type, *types):
    types = types or ()
    if None != _type:
        types = (_type,) + types

    if not value:
        raise ValueError("{} value is not set".format(name))
    if not types:
        return
    for t in types:
        if isinstance(value, t):
            return
    raise ValueError("{} value [{}] is not one of {}".format(name, value, types))


def env(key, default=None, transform=lambda x: x):
    """
    :type key: str
    :type default: str
    :type transform: lambda[str,T]
    :rtype: T
    """
    return transform(os.environ[key]) if key in os.environ else default


def int_env(key, default=None):
    """
    :param key: str
    :param default: int
    :rtype: int
    """
    return env(key, default=default, transform=lambda x: None if not x else int(x))


def bool_env(key, default=False):
    """
    :param key: str
    :param default: bool
    :rtype: bool
    """
    def __parse_bool(b):
        """
        :type b: str
        :rtype: bool
        """
        if not b:
            return default
        b = b.upper()
        if b == "1" or b == "Y" or b == "YES" or b == "T" or b == "TRUE":
            return True
        return False

    return env(key, default=default, transform=__parse_bool)


def list_env(key, default=()):
    """
    :type key: basestring
    :type default: tuple
    :rtype: tuple[str]
    """
    return env(key, default=default, transform=lambda l: tuple(l for l in l.split(",") if l))
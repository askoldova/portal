import os


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


def check_one_required(**kwargs):
    for k, v in kwargs.items():
        if v:
            return
    raise ValueError("One of {} have to be set".format(kwargs.keys()))


class HttpRedirect(Exception):
    def __init__(self, url):
        super(HttpRedirect, self).__init__()
        self.url = url

    def __str__(self):
        return self.url

    def __unicode__(self):
        return unicode(self.url)


def _check_type(name, value, *types):
    if not types:
        return

    for t in types:
        if isinstance(value, t):
            return
    raise ValueError("{} value [{}] is not one of {}".format(name, value, types))


def check_type(value, name, _type, *types):
    if value is None:
        return

    types = types or ()
    if _type is not None:
        types = (_type,) + types

    _check_type(name, value, *types)


def check_exist_and_type(value, name, _type, *types):
    if value is None:
        raise ValueError("{} value is not set".format(name))

    types = types or ()
    if _type is not None:
        types = (_type,) + types

    _check_type(name, value, *types)


def check_exist_and_type2(*types, **values):
    for name, v in values.items():
        if not v:
            raise ValueError("Value {} have to be set".format(name))

        _check_type(name, v, *types)


def check_string_value(**values):
    check_exist_and_type2(str, unicode, **values)


def check_int_value(**values):
    check_exist_and_type2(int, long, **values)


def check_type2(*types, **values):
    for name, v in values.items():
        if v is None:
            continue
        _check_type(name, v, *types)


def check_int(**values):
    check_type2(int, long, **values)


def check_string(**values):
    check_type2(str, unicode, **values)

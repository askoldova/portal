import os


def env(key, default=None, transform=lambda x: x):
    """
    :type key: str
    :type default: str
    :type transform: lambda[str,T]
    :rtype: T
    """
    return transform(os.environ[key]) if key in os.environ else default

# def env


def int_env(key, default=None):
    """
    :param key: str
    :param default: int
    :rtype: int
    """
    return env(key, default=default, transform=lambda x: None if not x else int(x))

# def int_env


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

# def bool_env

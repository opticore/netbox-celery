"""Functions for Django settings."""
import os
from distutils.util import strtobool  # pylint: disable=deprecated-module


def is_truthy(arg):
    """
    Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True

    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(str(arg)))


def parse_redis_connection(redis_database):
    """
    Parse environment variables to emit a Redis connection URL.

    Args:
        redis_database (int): Redis database number to use for the connection

    Returns:
        Redis connection URL (str)
    """
    # The following `_redis_*` variables are used to generate settings based on
    # environment variables.
    redis_scheme = (
        "rediss" if is_truthy(os.getenv("REDIS_SSL", False)) else "redis"  # pylint: disable=invalid-envvar-default
    )
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))  # pylint: disable=invalid-envvar-default
    redis_username = os.getenv("REDIS_USERNAME", "")
    redis_password = os.getenv("REDIS_PASSWORD", "")

    # Default Redis credentials to being empty unless a username or password is
    # provided. Then map it to "username:password@". We're not URL-encoding the
    # password because the Redis Python client already does this.
    redis_creds = ""
    if redis_username or redis_password:
        redis_creds = f"{redis_username}:{redis_password}@"

    return f"{redis_scheme}://{redis_creds}{redis_host}:{redis_port}/{redis_database}"

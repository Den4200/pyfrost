from typing import Callable, Optional
import json
import functools


@functools.lru_cache()
def get_auth_token() -> Optional[str]:
    """Returns the saved auth token.

    :return: The auth token saved in `.frost`
    :rtype: Optional[str]
    """
    with open('.frost', 'r') as f:
        return json.load(f).get('auth_token')


@functools.lru_cache()
def get_id() -> Optional[str]:
    """Returns the saved id.

    :return: The ID saved in `.frost`
    :rtype: Optional[str]
    """
    with open('.frost', 'r') as f:
        return json.load(f).get('id')


def get_auth(func: Callable) -> Callable:
    """A decorator to get the saved auth token and id.

    :param func: The function that is being wrapped
    :type func: Callable
    :return: The inner execute function
    :rtype: Callable
    """
    def execute(*args, **kwargs):
        """Executes the given function, passsing through the auth token and id.
        """
        return func(
            *args, **kwargs,
            token=get_auth_token(),
            id_=get_id()
        )
    return execute

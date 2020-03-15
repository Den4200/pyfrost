from typing import Callable
from functools import wraps

from frost.server.headers import Header
from frost.server.storage import User
from frost.server.headers import Status


def auth_required(func: Callable) -> Callable:
    """A decorator to ensure a client is logged in with valid authentication \
    before running the wrapped function. Automatically passes through \
    the user's ID (:code:`id_`) and token (:code:`token`) as arguments.

    :param func: The function being wrapped
    :type func: Callable
    :return: The inner execute function
    :rtype: Callable
    """
    @wraps(func)
    def execute(*args, **kwargs):
        id_ = args[0]['headers'].get(Header.ID_TOKEN.value)
        token = args[0]['headers'].get(Header.AUTH_TOKEN.value)

        if id_ is not None and token is not None:
            user = User.search(id_)

            if user is not None and user['token'] == token:
                return func(*args, **kwargs, id_=id_, token=token)

        return Status.INVALID_AUTH

    return execute

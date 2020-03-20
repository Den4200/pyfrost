from functools import wraps
from typing import Callable

from frost.server.headers import Status
from frost.server.database import managed_session, User


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
        id_ = args[0]['headers'].get('id')
        token = args[0]['headers'].get('token')

        with managed_session() as session:
            user = session.query(User).filter(
                User.id == id_,
                User.token == token
            ).first()

        if user is not None:
            return func(*args, **kwargs, id_=id_, token=token)

        return Status.INVALID_AUTH

    return execute

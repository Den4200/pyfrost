from typing import Any, Callable
from threading import Thread

from ..headers import Method


class threaded:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: Callable):

        def execute(*args: Any, **kwargs: Any):
            Thread(
                target=func,
                args=args,
                kwargs=kwargs,
                daemon=self.kwargs.get('daemon', False)
            ).start()

        return execute


def auth_required(func: Callable):

    def execute(*args: Any, **kwargs: Any) -> None:
        data = args[0]
        token = data.get(Header.AUTH_TOKEN.value)

        if token:
            pass

        # TODO

    return execute

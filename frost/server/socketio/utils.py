from functools import wraps
from threading import Thread
from typing import Any, Callable


class threaded:
    """A decorator to thread a function/method.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """The constructor method.
        """
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: Callable) -> Callable:
        """The __call__ method.

        :param func: The function that is being wrapped
        :type func: Callable
        :return: The inner execute function
        :rtype: Callable
        """
        @wraps(func)
        def execute(*args: Any, **kwargs: Any) -> None:
            """Starts the function in a new thread.
            """
            Thread(
                target=func,
                args=args,
                kwargs=kwargs,
                daemon=self.kwargs.get('daemon', False)
            ).start()

        return execute

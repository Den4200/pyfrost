from typing import Any, Callable
from threading import Thread


class threaded:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func: Callable):
        
        def execute(*args, **kwargs):
            Thread(
                target=func,
                args=args,
                kwargs=kwargs,
                daemon=self.kwargs.get('daemon', False)
            )

        return execute

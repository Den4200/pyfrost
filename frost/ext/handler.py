from typing import Any, Callable, Dict, Optional
from pathlib import Path

from frost.ext.cog import _cogs


class Handler:
    """Handles incoming requests and executes methods according to the route path mapping.

    :param send: Passes the send function over to the method called if given.
    :type send: Optional[Callable]
    """

    def __init__(self, send: Optional[Callable] = None) -> None:
        """The constructor method.
        """
        self.send = send

    @staticmethod
    def _handle_path(path: str) -> Callable:
        """Handles the path of the route and returns the resulting function.

        :param path: The route's path
        :type path: str
        :return: The resulting function
        :rtype: Callable
        """
        parts = Path(path).parts

        result = _cogs
        for part in parts:
            result = result[part]

        return result

    def handle(self, data: Dict[str, Any]) -> Any:
        """Handles the route and executes the resulting function.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        :return: Data returned from the executed function
        :rtype: Any
        """
        if self.send is None:
            return self._handle_path(data['headers']['path'])(data)

        return self._handle_path(data['headers']['path'])(self.send, data)
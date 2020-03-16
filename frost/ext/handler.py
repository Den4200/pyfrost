from pathlib import Path
from typing import Any, Callable, Dict

from frost.ext.cog import _cogs


class Handler:
    """Handles incoming requests and executes methods according to the route path mapping.
    """

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

    def handle(self, data: Dict[str, Any], **kwargs) -> None:
        """Handles the route and executes the resulting method.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        self._handle_path(data['headers']['path'])(data, **kwargs)

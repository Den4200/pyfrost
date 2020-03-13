from typing import Any, Callable, Dict
from pathlib import Path

from frost.server.ext.cog import _cogs


class Handler:

    def __init__(self, send: Callable) -> None:
        self.send = send

    @staticmethod
    def _handle_path(path: str) -> None:
        parts = Path(path).parts

        result = _cogs
        for part in parts:
            result = result[part]

        return result

    def handle(self, data: Dict[str, Any]) -> None:
        return self._handle_path(data['headers']['path'])(self.send, data)

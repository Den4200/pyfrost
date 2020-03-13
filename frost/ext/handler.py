from typing import Any, Callable, Dict, Optional
from pathlib import Path

from frost.ext.cog import _cogs


class Handler:

    def __init__(self, send: Optional[Callable] = None) -> None:
        self.send = send

    @staticmethod
    def _handle_path(path: str) -> None:
        parts = Path(path).parts

        result = _cogs
        for part in parts:
            result = result[part]

        return result

    def handle(self, data: Dict[str, Any]) -> None:
        if self.send is None:
            return self._handle_path(data['headers']['path'])(data)

        return self._handle_path(data['headers']['path'])(self.send, data)

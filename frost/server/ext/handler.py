from typing import Any
from pathlib import Path

from frost.server.ext.cog import _cogs


class Handler:

    def _handle_path(self, path: str) -> None:
        parts = Path(path).parts

        result = _cogs
        for part in parts:
            result = result[part]

        return result

    def handle(self, path: str, data: Any) -> None:
        method = self._handle_path(path)
        return method(data)

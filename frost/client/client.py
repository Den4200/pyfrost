from pathlib import Path
from .socketio import BaseClient


class FrostClient(BaseClient):

    def __init__(self, file: str) -> None:
        super(FrostClient, self).__init__()
        path = Path(file)

        self._name = path.name
        self._dir = path.parent

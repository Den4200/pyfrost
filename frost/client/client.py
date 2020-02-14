from pathlib import Path
from .socketio import BaseClient


class FrostClient(BaseClient):

    def __init__(self) -> None:
        super(FrostClient, self).__init__()

    def __enter__(self) -> None:
        self.connect()
        return self

    def __exit__(self, type_, value, traceback) -> None:
        self.close()

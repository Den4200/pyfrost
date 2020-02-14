from pathlib import Path

from .headers import Header, Method
from .methods import exec_method
from .socketio import BaseClient


class FrostClient(BaseClient):

    def __init__(self) -> None:
        super(FrostClient, self).__init__()

    def __enter__(self) -> None:
        self.connect()
        return self

    def __exit__(self, type_, value, traceback) -> None:
        self.close()

    def recieve(self) -> None:
        data = super(FrostClient, self).recieve()
        headers = data['headers']
        method = headers[Header.METHOD.value]

        resp = exec_method(method, data)
        print(resp)

from pathlib import Path

from .headers import Header, Method
from .methods import (
    exec_method,
    _store_id
)
from .socketio import BaseClient
from .auth import auth_required


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

    def login(self, id_, username, password) -> None:
        self.send({
            'headers': {
                Header.METHOD.value: Method.LOGIN.value
            },
            'id': id_,
            'username': username,
            'password': password
        })
        _store_id({'id': id_})
        self.recieve()

    @auth_required
    def send_msg(self, msg, token=None, id_=None) -> None:
        self.send({
            'headers': {
                Header.METHOD.value: Method.SEND_MSG.value,
                Header.AUTH_TOKEN.value: token,
                Header.ID_TOKEN.value: id_
            },
            'msg': msg
        })

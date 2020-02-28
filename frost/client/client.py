from typing import Any
import json

from .headers import Header, Method
from .methods import (
    exec_method,
    _store_id
)
from .socketio import BaseClient
from .auth import get_auth


class FrostClient(BaseClient):

    def __init__(self) -> None:
        super(FrostClient, self).__init__()

    def __enter__(self) -> None:
        self.connect()
        return self

    def __exit__(self, type_, value, traceback) -> None:
        self.close()

    def recieve(self) -> Any:
        data = super(FrostClient, self).recieve()
        headers = data['headers']
        method = headers[Header.METHOD.value]

        resp = exec_method(method, data)
        return resp

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

    def register(self, username, password) -> None:
        self.send({
            'headers': {
                Header.METHOD.value: Method.REGISTER.value
            },
            'username': username,
            'password': password
        })

    @get_auth
    def send_msg(self, msg, token=None, id_=None) -> None:
        self.send({
            'headers': {
                Header.METHOD.value: Method.SEND_MSG.value,
                Header.AUTH_TOKEN.value: token,
                Header.ID_TOKEN.value: id_
            },
            'msg': msg
        })

    @get_auth
    def get_all_msgs(self, token=None, id_=None) -> Any:
        self.send({
            'headers': {
                Header.METHOD.value: Method.GET_ALL_MSG.value,
                Header.AUTH_TOKEN.value: token,
                Header.ID_TOKEN.value: id_
            }
        })
        return self.recieve()

    @get_auth
    def get_new_msgs(self, token=None, id_=None):
        with open('.frost', 'r') as f:
            last = json.load(f).get('last_msg_timestamp')

        self.send({
            'headers': {
                Header.METHOD.value: Method.GET_NEW_MSG.value,
                Header.AUTH_TOKEN.value: token,
                Header.ID_TOKEN.value: id_
            },
            'last_msg_timestamp': last
        })
        
        return self.recieve()

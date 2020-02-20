from typing import Callable
from pathlib import Path
import secrets
import struct

from .room import Room
from .user import User
from .methods import exec_method
from .headers import Header, Method
from .socketio import BaseServer, threaded


class FrostServer(BaseServer):
    """
    The Frost server.
    """

    def __init__(self, file: str) -> None:
        super(FrostServer, self).__init__()
        path = Path(file)

        self._name = path.name
        self._dir = path.parent

        self.config = {
            'AFK_TIMEOUT': 900,
        }

        self._rooms = list()

        self.func = self._on_user_connect

    def room(self, *deco_args, **deco_kwargs) -> Callable:

        def inner(func) -> Callable:

            def execute(*args, **kwargs):
                room = Room(*deco_args, **deco_kwargs)
                self._rooms.append(room)
                return func(room)

            return execute

        return inner

    @threaded()
    def _on_user_connect(self, conn: 'socket.socket', addr):
        while True:
            try:
                data = self.recieve(conn)
            
            except struct.error:
                break

            else:
                headers = data['headers']
                method = headers[Header.METHOD.value]

                resp = exec_method(method, data)

                if method == Method.LOGIN.value:
                    self.send(conn, {
                        'headers': {
                            Header.METHOD.value: Method.NEW_TOKEN.value
                        },
                        'auth_token': resp
                    })

                elif method == Method.REGISTER.value:
                    self.send(conn, {
                        'headers': {
                            Header.METHOD.value: Method.NEW_ID.value
                        },
                        'id': resp
                    })

    def run(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """
        Runs the Frost Server.
        """
        self.ip = ip
        self.port = port
        
        self.start()

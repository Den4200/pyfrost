from typing import Any, Callable, Tuple
from functools import wraps
from pathlib import Path
import struct
import socket
import json

from frost.server.room import Room
from frost.server.ext import Handler
from frost.server.socketio import BaseServer, threaded
from frost.server.storage.defaults import DEFAULT_FORMAT


def send_partial(send_func: Callable, conn: 'socket.socket') -> Callable:

    def execute(*args: Any, **kwargs: Any) -> Any:
        return send_func(conn, *args, **kwargs)

    return execute


class FrostServer(BaseServer):
    """The Frost server.

    :param file: The :code:`__file__` of the file this is imported in
    :type file: str
    """

    def __init__(self, file: str) -> None:
        super(FrostServer, self).__init__()
        path = Path(file)

        self._name = path.name
        self._dir = path.parent

        self._rooms = list()

        self.func = self.on_user_connect

        storage = Path('storage.json')
        if not storage.exists():
            with open(str(storage), 'w') as f:
                json.dump(DEFAULT_FORMAT, f, indent=2)

    def room(self, *deco_args: Any, **deco_kwargs: Any) -> Callable:
        """Create a room.

        :raises NotImplementedError: This decorator is not implemented yet
        """
        raise NotImplementedError

        def inner(func) -> Callable:
            @wraps(func)
            def execute(*args: Any, **kwargs: Any) -> Any:
                room = Room(*deco_args, **deco_kwargs)
                self._rooms.append(room)
                return func(room)

            return execute

        return inner

    @threaded()
    def on_user_connect(self, conn: 'socket.socket', addr: Tuple[str, int]) -> None:
        """Handles the connection of a client and executes tasks accordingly.

        :param conn: The client's connection
        :type conn: socket.socket
        :param addr: The user's IP address and port
        :type addr: Tuple[str, int]
        """
        handler = Handler(send_partial(self.send, conn))

        while True:
            try:
                data = self.recieve(conn)

            except struct.error:
                break

            else:
                handler.handle(data)

    def run(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """Runs the FrostServer.

        :param ip: The IP for the server to bind to, defaults to '127.0.0.1'
        :type ip: str, optional
        :param port: The port for the server to bind to, defaults to 5555
        :type port: int, optional
        """
        self.ip = ip
        self.port = port

        self.start()

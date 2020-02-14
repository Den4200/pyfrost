from typing import Callable
from pathlib import Path
import struct

from .database import db_session
from .room import Room
from .user import User
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
                username = data['username']
                password = data['password']
                
                print(username, password)

    def run(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """
        Runs the Frost Server.
        """
        self.ip = ip
        self.port = port
        
        self.start()

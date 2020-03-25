import socket
from pathlib import Path
from typing import Any, Callable, Tuple

from frost.ext import Handler
from frost.server.cogs import Auth, Msgs, Rooms
from frost.server.objects import Memory, UserObj
from frost.server.socketio import BaseServer, threaded


def send_partial(send_func: Callable, conn: 'socket.socket') -> Callable:
    """A partial function to auto fill the :code:`conn` parameter of \
    :meth:`frost.server.socketio.base_server.BaseServer`

    :param send_func: The send function that sends data to the client
    :type send_func: Callable
    :param conn: A specific client's connection
    :type conn: socket.socket
    :return: The inner execute function
    :rtype: Callable
    """

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

        # Load up the cogs
        Auth()
        Msgs()
        Rooms()

        path = Path(file)

        self._name = path.name
        self._dir = path.parent

        self.func = self.on_user_connect

        db = Path('pyfrost.sqlite3')
        if not db.exists():
            from frost.server.database import init_db
            init_db()

    @threaded()
    def on_user_connect(self, conn: 'socket.socket', addr: Tuple[str, int]) -> None:
        """Handles the connection of a client and executes tasks accordingly.

        :param conn: The client's connection
        :type conn: 'socket.socket'
        :param addr: The user's IP address and port
        :type addr: Tuple[str, int]
        """
        user = UserObj(addr, conn)
        Memory.all_users[addr] = user

        handler = Handler()

        while True:
            try:
                data = self.recieve(conn)

            except Exception:
                Memory.all_users.pop(addr)

                for id_, auth_user in Memory.logged_in_users.items():
                    if auth_user.addr == addr:
                        Memory.logged_in_users.pop(id_)
                        break

                break

            else:
                handler.handle(
                    data,
                    addr=addr,
                    send=self.send,
                    client_send=send_partial(self.send, conn)
                )

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

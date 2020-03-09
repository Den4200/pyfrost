from typing import (
    Any,
    Tuple,
    Optional,
    Callable
)
import time
import pickle
import socket
import struct
from dataclasses import dataclass

from frost.server.socketio.utils import threaded
from frost.server.logger import logger


@dataclass
class ConnectionData:
    conn: Optional['socket.socket'] = None
    addr: Optional[Tuple[str, int]] = None


class BaseServer:
    """A basic socket server to send and receive data from multiple clients. \
    Assign self.func to a method with :code:`conn, addr` as parameters \
    to handle new user connections, as shown in \
    :meth:`frost.server.server.FrostServer.on_user_connect`

    :param ip: The IP address for the server to bind to, defaults to '127.0.0.1'
    :type ip: str, optional
    :param port: The port for the server to bind to, defaults to 5555
    :type port: int, optional
    """

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """The constructor method.
        """
        self.ip = ip
        self.port = port
        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.func: Optional[Callable] = None

    def send(self, conn: 'socket.socket', data: Any) -> None:
        """Send data to a specific connected client.

        :param conn: The connected client socket
        :type conn: socket.socket
        :param data: The data to send to the client
        :type data: Any
        """
        packets = pickle.dumps(data, protocol=0)
        value = socket.htonl(len(packets))
        size = struct.pack('L', value)

        conn.send(size)
        conn.send(packets)

    def recieve(self, conn: 'socket.socket') -> Any:
        """Receive data from a specific client.

        :param conn: The connected client socket
        :type conn: socket.socket
        :return: The data received from the client
        :rtype: Any
        """
        size = struct.calcsize('L')
        size = conn.recv(size)
        size = socket.ntohl(struct.unpack('L', size)[0])

        result = b''

        while len(result) < size:
            result += conn.recv(size - len(result))

        return pickle.loads(result)

    @threaded(daemon=True)
    def _accept_conn(self, conn_data_cls: 'ConnectionData') -> None:
        """Waits for a connection on a separate thread and accepts them. \
        Done this way to be able to stop the server.

        :param conn_data_cls: Where to save the client socket data on accept.
        :type conn_data_cls: ConnectionData
        """
        conn_data_cls.conn, conn_data_cls.addr = self._socket.accept()

    def start(self) -> None:
        """Starts the threaded, multi-client Server.
        """
        try:
            self._socket.bind((self.ip, self.port))

        except socket.error as e:
            print(e)

        else:
            self._socket.listen()
            logger.info('Server is online!')

            run = True
            while run:
                conn_data = ConnectionData()
                self._accept_conn(conn_data)

                # Makes the server stoppable
                while conn_data.conn is None or conn_data.addr is None:
                    try:
                        time.sleep(0.1)
                    except KeyboardInterrupt:
                        run = False
                        break

                conn, addr = conn_data.conn, conn_data.addr
                logger.info(f'Connection established to {addr}')

                if self.func is not None:
                    self.func(conn, addr)

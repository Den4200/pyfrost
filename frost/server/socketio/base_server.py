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
    """
    A basic sockets server to send and receive
    data from multiple clients.
    """

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        self.ip = ip
        self.port = port
        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.func: Optional[Callable] = None

    def send(self, conn: 'socket.socket', data: Any) -> None:
        packets = pickle.dumps(data, protocol=0)
        value = socket.htonl(len(packets))
        size = struct.pack('L', value)

        conn.send(size)
        conn.send(packets)

    def recieve(self, conn: 'socket.socket') -> Any:
        size = struct.calcsize('L')
        size = conn.recv(size)
        size = socket.ntohl(struct.unpack('L', size)[0])

        result = b''

        while len(result) < size:
            result += conn.recv(size - len(result))

        return pickle.loads(result)

    @threaded(daemon=True)
    def _accept_conn(self, conn_data_cls: 'ConnectionData') -> None:
        """
        Waits for a connection on a separate
        thread and accepts them.
        """
        conn_data_cls.conn, conn_data_cls.addr = self._socket.accept()

    def start(self) -> None:
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

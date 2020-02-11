from typing import Any, Tuple, Optional
import pickle
import socket
import struct
from dataclasses import dataclass

from .utils import threaded


@dataclass
class ConnectionData:
    conn: Optional['socket.socket'] = None
    addr: Optional[Tuple[str, int]] = None


class Server:
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
        self.func = None

    def send(self, conn: 'socket.socket', data: Any) -> None:
        packets = pickle.dumps(data)
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
        """
        
        """
        try:
            self._socket.bind((self.ip, self.port))

        except socket.error as e:
            print(e)

        else:
            print('Server sucessfully initialized')
            self._socket.listen()
            print('Server awaiting new connections')

            run = True
            while run:
                conn_data = ConnectionData()
                self._accept_conn(conn_data)
                
                # Makes the server stoppable
                while conn_data.conn is None or conn_data.addr is None:
                    try:
                        pass
                    except KeyboardInterrupt:
                        run = False
                        break

                conn, addr = conn_data.conn, conn_data.addr
                print(f'Connection established to {addr}')

                if self.func is not None:
                    self.func(conn, addr)

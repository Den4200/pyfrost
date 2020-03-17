import json
import socket
import struct
from typing import Any


class BaseClient:
    """The base client to connect to a server & send and receive data.

    :param ip: The IP address of the server to connect to, defaults to '127.0.0.1'
    :type ip: str, optional
    :param port: The port of the server to connect to, defaults to 5555
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

    def connect(self) -> None:
        """Connect and establish a connect to the server.
        """
        self._socket.connect((self.ip, self.port))

    def close(self) -> None:
        """Close the connection to the server.
        """
        self._socket.close()

    def recieve(self) -> Any:
        """Recieve data from the server.

        :return: Data received from the server
        :rtype: Any
        """
        size = struct.calcsize('L')
        size = self._socket.recv(size)
        size = socket.ntohl(
            struct.unpack('L', size)[0]
        )

        result = b''

        while len(result) < size:
            result += self._socket.recv(size - len(result))

        return json.loads(result)

    def send(self, data: Any) -> None:
        """Send data to the server.

        :param data: Data to send to the server
        :type data: Any
        """
        packets = json.dumps(data).encode('utf-8')
        value = socket.htonl(len(packets))
        size = struct.pack('L', value)
        self._socket.send(size)
        self._socket.send(packets)

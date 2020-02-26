from typing import Any

import pickle
import socket
import struct


class BaseClient:

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        self.ip = ip
        self.port = port
        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def connect(self) -> None:
        self._socket.connect((self.ip, self.port))

    def close(self) -> None:
        self._socket.close()

    def recieve(self) -> Any:
        size = struct.calcsize('L')
        size = self._socket.recv(size)
        size = socket.ntohl(
            struct.unpack('L', size)[0]
        )

        result = b''

        while len(result) < size:
            result += self._socket.recv(size - len(result))

        return pickle.loads(result)

    def send(self, data: Any) -> None:
        packets = pickle.dumps(data)
        value = socket.htonl(len(packets))
        size = struct.pack('L', value)
        self._socket.send(size)
        self._socket.send(packets)

import socket
from typing import Tuple


class UserObj:

    def __init__(
        self,
        addr: Tuple[str, int],
        conn: 'socket.socket',
        id_=None,
        username=None
    ) -> None:
        self.addr = addr
        self.conn = conn
        self.id = id_
        self.username = username

    @property
    def is_logged_in(self) -> bool:
        return self.id is not None and self.username is not None

    def login(self, id_, username) -> None:
        self.id = id_
        self.username = username


class Memory:
    all_users = dict()
    logged_in_users = dict()

import socket
from typing import Optional, Tuple


class UserObj:
    """Represents a user.

    :param addr: The IP address and port of the connected user
    :type addr: Tuple[str, int]
    :param conn: The socket instance of the connected user
    :type conn: 'socket.socket'
    :param id_: The user's ID, defaults to None
    :type id_: Optional[int]
    :param username: The user's username, defaults to None
    :type username: Optional[str]
    """

    def __init__(
        self,
        addr: Tuple[str, int],
        conn: 'socket.socket',
        id_: Optional[int] = None,
        username: Optional[str] = None
    ) -> None:
        """The constructor method.
        """
        self.addr = addr
        self.conn = conn
        self.id = id_
        self.username = username

    @property
    def is_logged_in(self) -> bool:
        """Returns whether or not the user is logged in.

        :return: Whether or not the user is logged in
        :rtype: bool
        """
        return self.id is not None and self.username is not None

    def login(self, id_: int, username: str) -> None:
        """Sets the user's ID and username, "logging them in".

        :param id_: The user's ID
        :type id_: int
        :param username: The user's username
        :type username: str
        """
        self.id = id_
        self.username = username


class Memory:
    """Stores information that needs to be passed around and easily accessible.
    """
    all_users = dict()
    """All connected users.
    """
    logged_in_users = dict()
    """All logged in users.
    """

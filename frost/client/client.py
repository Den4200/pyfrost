import json
from pathlib import Path

from frost.client.auth import get_auth
from frost.client.events import (
    Auth,
    Msgs,
    messages
)
from frost.client.socketio import BaseClient, threaded
from frost.ext import Handler


class FrostClient(BaseClient):
    """The Frost Client.

    :param ip: The IP address of the server to connect to, defaults to '127.0.0.1'
    :type ip: str, optional
    :param port: The port of the server to connect to, defaults to 5555
    :type port: int, optional
    """

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555) -> None:
        """The constructor method.
        """
        super(FrostClient, self).__init__(ip, port)

        # Load up cogs
        Auth()
        Msgs()

        frost_file = Path('.frost')

        if not frost_file.exists():
            with open(str(frost_file), 'w') as f:
                json.dump({}, f)

    def __enter__(self) -> 'FrostClient':
        """The __enter__ method, connects to the server.

        :return: This instance of this class
        :rtype: 'FrostClient'
        """
        self.connect()
        return self

    def __exit__(self, type_, value, traceback) -> None:
        """The __exit__ method, closes the connection to the server.
        """
        self.close()

    def connect(self) -> None:
        """Connect to the server and begin listening for events.
        """
        super().connect()
        self._listen()

    @threaded(daemon=True)
    def _listen(self) -> None:
        """Listen for events and handle them.
        """
        handler = Handler()

        while True:
            handler.handle(self.recieve())

    def login(self, username: str, password: str) -> None:
        """Login to the server.

        :param username: The username of the account
        :type username: str
        :param password: The password of the account
        :type password: str
        """
        self.send({
            'headers': {
                'path': 'authentication/login'
            },
            'username': username,
            'password': password
        })

    def register(self, username: str, password: str) -> None:
        """Register an account on the server.

        :param username: The desired username of the account
        :type username: str
        :param password: The desired password of the account
        :type password: str
        """
        self.send({
            'headers': {
                'path': 'authentication/register'
            },
            'username': username,
            'password': password
        })

    @get_auth
    def send_msg(self, msg: str, token: str, id_: str) -> None:
        """Send a message to other users on the server.

        :param msg: The desired message to send
        :type msg: str
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'token': token,
                'id': id_,
                'path': 'messages/send_msg'
            },
            'msg': msg
        })

    @get_auth
    def get_all_msgs(
        self,
        token: str,
        id_: str
    ) -> None:
        """Get all messages from the server. Should not be needed.

        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        :return: All messages
        :rtype: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
        """
        messages.clear()
        self.send({
            'headers': {
                'path': 'messages/get_all_msgs',
                'token': token,
                'id': id_
            }
        })

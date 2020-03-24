import json
from pathlib import Path

from frost.client.auth import get_auth
from frost.client.events import (
    Auth,
    Msgs,
    Rooms
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
        Rooms()

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
    def send_msg(self, room_id: int, msg: str, token: str, id_: str) -> None:
        """Send a message to other users on a server in a specific room.

        :param room_id: The ID of the room to send the message to
        :type room_id: int
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
            'msg': msg,
            'room_id': room_id
        })

    @get_auth
    def get_room_msgs(
        self,
        room_id: int,
        token: str,
        id_: str
    ) -> None:
        """Get all messages from a specific room in a server.

        :param room_id: The ID of the room to get the messages from
        :type room_id: int
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'messages/get_room_msgs',
                'token': token,
                'id': id_
            },
            'room_id': room_id
        })

    @get_auth
    def create_room(
        self,
        room_name: str,
        token: str,
        id_: str
    ) -> None:
        """Create a new room in a server.

        :param room_name: The name of the room to create
        :type room_name: str
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/create',
                'token': token,
                'id': id_
            },
            'room_name': room_name
        })

    @get_auth
    def join_room(
        self,
        invite_code: str,
        token: str,
        id_: str
    ) -> None:
        """Join a room in a server with an invite code.

        :param invite_code: The invite code the room to join
        :type invite_code: str
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/join',
                'token': token,
                'id': id_
            },
            'invite_code': invite_code
        })

    @get_auth
    def leave_room(
        self,
        room_id: int,
        token: str,
        id_: str
    ) -> None:
        """Leave a joined room in a server.

        :param room_id: The ID of the room to leave
        :type room_id: int
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/leave',
                'token': token,
                'id': id_
            },
            'room_id': room_id
        })

    @get_auth
    def get_invite_code(
        self,
        room_id: int,
        token: str,
        id_: str
    ) -> None:
        """Get the invite code of a room in a server.

        :param room_id: The ID of the room to get an invite code from
        :type room_id: int
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/get_invite_code',
                'token': token,
                'id': id_
            },
            'room_id': room_id
        })

    @get_auth
    def get_joined_rooms(
        self,
        token: str,
        id_: str
    ) -> None:
        """Get all the joined rooms of the currently logged in user.

        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/get_all_joined',
                'token': token,
                'id': id_
            }
        })

    @get_auth
    def get_room_members(
        self,
        room_id: int,
        token: str,
        id_: str
    ) -> None:
        """Get all the members of a specific room.

        :param room_id: The ID of the room to get the members of
        :type room_id: int
        :param token: The user's token, auto filled by :meth:`frost.client.auth.get_auth`
        :type token: str
        :param id_: The user's ID, auto filled by :meth:`frost.client.auth.get_auth`
        :type id_: str
        """
        self.send({
            'headers': {
                'path': 'rooms/get_members',
                'token': token,
                'id': id_
            },
            'room_id': room_id
        })

import json
from typing import Any, Dict

from frost.client.events.events import EventStatus, Memory, Messages
from frost.client.headers import Status
from frost.ext import Cog


class Auth(Cog, route='authentication'):
    """Deals with user authentication. :code:`route='authentication'`
    """

    def post_register(data: Dict[str, Any]) -> None:
        """Deals with the response received from the server after a registration attempt.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        EventStatus.register = data['headers']['status']

    def post_login(data: Dict[str, Any]) -> None:
        """Deals with the response received from the server after a login attempt.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            with open('.frost', 'r') as f:
                contents = json.load(f)

            contents.update({
                'id': data['id'],
                'token': data['token']
            })

            with open('.frost', 'w') as f:
                json.dump(contents, f, indent=2)

        EventStatus.login = status


class Msgs(Cog, route='messages'):
    """Deals with user messages. :code:`route='messages'`
    """

    def new(data: Dict[str, Any]) -> None:
        """Deals with new user messages and stores them in :class:`frost.client.events.events.Messages`.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        Messages.add_new_msgs(data['msg'])

    def post_get_all(data: Dict[str, Any]) -> None:
        EventStatus.get_all_msgs = data['headers']['status']


class Rooms(Cog, route='rooms'):

    def post_create(data: Dict[str, Any]) -> None:
        EventStatus.create_room = data['headers']['status']

    def post_join(data: Dict[str, Any]) -> None:
        EventStatus.join_room = data['headers']['status']

    def post_leave(data: Dict[str, Any]) -> None:
        EventStatus.leave_room = data['headers']['status']

    def post_invite_code(data: Dict[str, Any]) -> None:
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            Memory.invite_codes[data['room_id']] = data['room_invite_code']

        EventStatus.get_invite_code = status

    def post_all_joined(data: Dict[str, Any]) -> None:
        Memory.rooms = data['rooms']
        EventStatus.get_all_joined_rooms = data['headers']['status']

    def post_members(data: Dict[str, Any]) -> None:
        pass

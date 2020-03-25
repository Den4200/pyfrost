import json
from typing import Any, Dict

from frost.client.events.events import EventStatus, Messages
from frost.client.objects import Memory
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

    def post_new(data: Dict[str, Any]) -> None:
        """Stores the response status of a send message attempt.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        EventStatus.send_msg = data['headers']['status']

    def post_room(data: Dict[str, Any]) -> None:
        """Deals with the post response from requesting all messages in a specific room. \
        Messages are stored in :class:`frost.client.events.events.Messages`.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        EventStatus.get_room_msgs = data['headers']['status']


class Rooms(Cog, route='rooms'):
    """Deals with room within a server. :code:`route='rooms'`
    """

    def post_create(data: Dict[str, Any]) -> None:
        """Deals with the post response from a room creation request.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        EventStatus.create_room = data['headers']['status']

    def post_join(data: Dict[str, Any]) -> None:
        """Deals with the post response from a join room request.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            Memory.add_rooms(data['room'])

        EventStatus.join_room = status

    def post_leave(data: Dict[str, Any]) -> None:
        """Deals with the post response from a leave room request.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            Memory.rooms.pop(data['room_id'])

        EventStatus.leave_room = data['headers']['status']

    def post_invite_code(data: Dict[str, Any]) -> None:
        """Deals with the post response from a room invite code request.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            Memory.set_invite_code(data['room_id'], data['room_invite_code'])

        EventStatus.get_invite_code = status

    def post_all_joined(data: Dict[str, Any]) -> None:
        """Deals with the post response from a request for all joined rooms.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        Memory.add_rooms(*data['rooms'])
        EventStatus.get_joined_rooms = data['headers']['status']

    def post_members(data: Dict[str, Any]) -> None:
        """Deals with the post response from a request for all members in a room.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        status = data['headers']['status']

        if status == Status.SUCCESS.value:
            Memory.add_room_members(data['room_id'], *data['members'])

        EventStatus.get_room_members = status

    def new_room_member(data: Dict[str, Any]) -> None:
        """Adds a member to a specific room when they join.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        Memory.add_room_members(data['room_id'], data['user'])

    def remove_room_member(data: Dict[str, Any]) -> None:
        """Removes a member from a specific room when they leave.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        Memory.remove_room_member(data['room_id'], data['user_id'])

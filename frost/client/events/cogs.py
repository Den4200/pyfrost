import json
from typing import Any, Dict

from frost.client.events.events import login_status, messages, register_status
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
        register_status.current_status = data['headers']['status']

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

        login_status.current_status = status


class Msgs(Cog, route='messages'):
    """Deals with user messages. :code:`route='messages'`
    """

    def new(data: Dict[str, Any]) -> None:
        """Deals with new user messages and stores them in :class:`frost.client.events.events.Messages`.

        :param data: Data received from the server
        :type data: Dict[str, Any]
        """
        messages.add_new_msgs(data['msg'])

    def post_get_all(data: Dict[str, Any]) -> None:
        pass


class Rooms(Cog, route='rooms'):

    def post_create(data: Dict[str, Any]) -> None:
        pass

    def post_join(data: Dict[str, Any]) -> None:
        pass

    def post_leave(data: Dict[str, Any]) -> None:
        pass

    def post_invite_code(data: Dict[str, Any]) -> None:
        pass

    def post_all_joined(data: Dict[str, Any]) -> None:
        pass
